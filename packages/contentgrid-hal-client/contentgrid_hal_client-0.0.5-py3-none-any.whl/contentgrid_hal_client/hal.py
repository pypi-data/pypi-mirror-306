from http import HTTPStatus
from json import JSONDecodeError
import json
import logging
import re
from typing import List, Optional
from urllib.parse import urljoin
import uri_template
import requests
from requests.adapters import Retry, HTTPAdapter
from .exceptions import BadRequest, MissingHALTemplate, Unauthorized
from .token_utils import get_application_token

class HALLink:
    def __init__(self, uri: str, name: Optional[str] = None, title: Optional[str] = None, link_relation: Optional[str] = None) -> None:
        self.name: Optional[str] = name
        self.title: Optional[str] = title
        self.uri: str = uri
        self.link_relation = link_relation

class CurieRegistry:
    def __init__(self, curies: List[dict]) -> None:
        self.curies = {
            curie["name"]: Curie(curie["name"], curie["href"]) for curie in curies
        }

    def expand_curie(self, rel):
        if ":" in rel:
            prefix, suffix = rel.split(":", 1)
            if prefix in self.curies.keys():
                return uri_template.URITemplate(self.curies[prefix].url_template).expand(
                    rel=suffix
                )
        return rel

    def compact_curie(self, link: str):
        for curie in self.curies.values():
            variable_names = re.findall(r'{(.*?)}', curie.url_template)
            pattern = re.sub(r'{(.*?)}', r'(?P<\g<1>>.+)',  curie.url_template)
            match = re.match(pattern, link)
            if match:
                extracted_values = match.groupdict()
                variable_map = {variable_names[i]: extracted_values[variable_names[i]] for i in range(len(variable_names))}
                if "rel" in variable_map.keys():
                    return f"{curie.prefix}:{variable_map['rel']}"
        return link
    
class Curie:
    def __init__(self, prefix: str, url_template: str) -> None:
        assert uri_template.validate(template=url_template)
        self.url_template = url_template
        self.url_prefix = str(uri_template.URITemplate(url_template).expand(rel=''))
        self.prefix = prefix

class HALResponse:
    def __init__(self, data: dict, curie_registry: CurieRegistry = None) -> None:
        self.data: dict = data
        self.links: dict = data.get("_links", None)
        if self.links == None:
            logging.warning(f"HALresponse [type {type(self)}] did not have a _links field.")
        if self.links and "curies" in self.links.keys():
            self.curie_registry: CurieRegistry = CurieRegistry(self.links["curies"])
        elif curie_registry != None:
            self.curie_registry: CurieRegistry = curie_registry
        else:
            self.curie_registry = CurieRegistry(curies=[])
        
        self.embedded: dict = data.get("_embedded", None)
        self.templates: dict = data.get("_templates", None)
        self.metadata = {
            key: value
            for key, value in data.items()
            if not key.startswith("_")
        }

    def has_link(self, linkrel : str) -> bool:
        return len(self.get_links(linkrel=linkrel)) > 0
    
    def get_link(self, linkrel: str) -> HALLink:
        if self.has_link(linkrel=linkrel):
            if linkrel in self.links.keys():
                value = self.links[linkrel]
                if type(value) == list:
                    raise Exception(f"Linkrel {linkrel} was multivalued. Use get_links instead.")
            return self.get_links(linkrel=linkrel)[0]
        else:
            return None

    def get_links(self, linkrel: str) -> List[HALLink]:
        full_linkrel = linkrel
        # compact linkrel if curie registry is available.
        if self.curie_registry:
            linkrel = self.curie_registry.compact_curie(linkrel)

        if linkrel in self.links.keys():
            value = self.links[linkrel]
            if type(value) == list:
                return [
                    HALLink(
                        name=v.get("name", None),
                        title=v.get("title", None),
                        uri=v["href"],
                        link_relation=full_linkrel
                    )
                    for v in value
                ]
            elif type(value) == dict:
                return [ 
                    HALLink(
                        name=value.get("name", None),
                        title=value.get("title", None),
                        uri=value["href"],
                        link_relation=full_linkrel
                    )
                ]
                
            else:
                raise Exception(f"Unkown HALLINK type {type(value)}")
        else:
            return []
    
    def get_embedded_objects_by_key(self, key : str, infer_type:type = None) -> Optional[List["HALResponse"]]:
        if self.embedded:
            if not infer_type:
                infer_type = HALResponse
            return [
                infer_type(data=v, curie_registry=self.curie_registry)
                for v in self.embedded[self.curie_registry.compact_curie(key)]
            ]
        else:
            return []

    def get_self_link(self) -> HALLink:
        return self.get_link("self")
    
    def get_template(self, template_name : str) -> dict:
        if self.templates and template_name in self.templates.keys():
            return self.templates[template_name]
        else:
            raise MissingHALTemplate(f"HALForms template : {template_name} not found. User might not have permission or resource is of imcompatible type.")
    
    def __str__(self) -> str:
        return json.dumps(self.data, indent=4)
    
class InteractiveHALResponse(HALResponse):
    def __init__(self, data: dict, client: "HALFormsClient", curie_registry: CurieRegistry = None) -> None:
        super().__init__(data, curie_registry)
        self.client : "HALFormsClient" = client

    def get_embedded_objects_by_key(self, key, infer_type:type = None) -> Optional[List[HALResponse]]:
        if self.embedded:
            if not infer_type:
                infer_type = InteractiveHALResponse

            if issubclass(infer_type, InteractiveHALResponse):
                return [
                    infer_type(data=v, client=self.client, curie_registry=self.curie_registry)
                    for v in self.embedded[self.curie_registry.compact_curie(key)]
                ]
            else:
                return [
                    infer_type(data=v, curie_registry=self.curie_registry)
                    for v in self.embedded[self.curie_registry.compact_curie(key)]
                ]
        else:
            return []
        
    # Common operations
    def refetch(self):
        response = self.client.follow_link(self.get_self_link())
        self.__init__(data=response.data, client=self.client, curie_registry=self.curie_registry)

    def delete(self):
        response = self.client.delete(self.get_self_link().uri)
        self.client._validate_non_json_response(response)

    def put_data(self, data : dict) -> None:
        response = self.client.put(self.get_self_link().uri, json=data, headers={"Content-Type" : "application/json"})
        data = self.client._validate_json_response(response)
        # Reintialize class based on response data
        self.__init__(data=data, client=self.client, curie_registry=self.curie_registry)

    def patch_data(self, data : dict) -> None:
        response = self.client.patch(self.get_self_link().uri, json=data, headers={"Content-Type" : "application/json"})
        data = self.client._validate_json_response(response)
        # Reintialize class based on response data
        self.__init__(data=data, client=self.client, curie_registry=self.curie_registry)


class HALFormsClient(requests.Session):
    def __init__(self,
        client_endpoint: str,
        auth_uri: str = None,
        client_id: str = None,
        client_secret: str = None,
        token: str = None,
        session_cookie : str = None,
        pool_maxsize : int = 10,
    ) -> None:
        super().__init__()
        self.token = token
        self.session_cookie = session_cookie.replace("SESSION=","") if session_cookie else None

        self.client_endpoint = client_endpoint
        self.auth_uri = auth_uri

        # Retries requests for status_forcelist response codes with backoff factor increasing wait time between each request
        retries = Retry(total=5,
                backoff_factor=0.2,
                status_forcelist=[ 500, 502, 503, 504 ])
        
        self.mount('http://', HTTPAdapter(max_retries=retries, pool_maxsize=pool_maxsize))

        # Service account
        self.client_id = client_id
        self.client_secret = client_secret

        self.has_service_account = self.client_id and self.client_secret

        logging.info(f"ContentGrid deployment endpoint: {self.client_endpoint}")
        logging.info(f"ContentGrid Auth URI: {self.auth_uri}")
        if self.has_service_account:
            logging.info(f"ContentGrid service account used...")
            logging.info(
                f"\t - Client id: {self.client_id}, Client secret: {self.client_secret[:4]}****..."
            )
            if not self.auth_uri:
                raise Exception("Auth URI is required when using a service account")
            logging.info("Fetching session token...")
            self.headers["Authorization"] = (
                f"Bearer {get_application_token(auth_uri=self.auth_uri, client_id=self.client_id, client_secret=self.client_secret)}"
            )
        elif self.token:
            self.headers["Authorization"] = f"Bearer {self.token}"
        elif self.session_cookie:
            self.cookies.set(name="SESSION", value=self.session_cookie)
        else:
            raise Exception("Token or Service account (client_id & client_secret) is required.")
        
        self.headers["Accept"] = "application/prs.hal-forms+json"
        logging.info(f"Client Cookies : {self.cookies.items()}")

    def _transform_hal_links_to_uris(self, attributes : dict) -> None:
        for attribute, value in attributes.items():
            if isinstance(value, list):
                for i, v in enumerate(value):
                    if isinstance(v, HALLink):
                        attributes[attribute][i] = v.uri
            else:
                if isinstance(value, HALLink):
                    attributes[attribute] = value.uri

    def _create_text_uri_list_payload(self, links : List[str | HALLink | HALResponse]) -> str:
        uri_list = []
        for link in links:
            if isinstance(link, HALLink):
                uri_list.append(link.uri)
            elif isinstance(link, HALResponse):
                uri_list.append(link.get_self_link().uri)
            elif isinstance(link, str):
                uri_list.append(link)
            else:
                raise BadRequest(f"Incorrect Link type {type(link)} in uri list payload, allowed types: HALLink, HALResponse or str")
        return "\n".join(uri_list)

    def _validate_non_json_response(self, response: requests.Response) -> requests.Response:
        self._raise_for_status(response)
        return response
    
    def _validate_json_response(self, response: requests.Response) -> dict | str:
        self._raise_for_status(response)
        if response.status_code < 300:
            try:
                return response.json()
            except JSONDecodeError as e:
                logging.error(f"Failed to parse JSON, error: {str(e)}")
                return response.content
    
    def _raise_for_status(self, response: requests.Response):
        """Raises :class:`HTTPError`, if one occurred."""

        http_error_msg = ""
        if hasattr(response, "reason") and isinstance(response.reason, bytes):
            # We attempt to decode utf-8 first because some servers
            # choose to localize their reason strings. If the string
            # isn't utf-8, we fall back to iso-8859-1 for all other
            # encodings. (See PR #3538)
            try:
                reason = response.reason.decode("utf-8")
            except UnicodeDecodeError:
                reason = response.reason.decode("iso-8859-1")
        else:
            if hasattr(response, "reason"):
                reason = response.reason
            else:
                reason = "reason unknown"

        if 400 <= response.status_code < 500:
            http_error_msg = (
                f"{response.status_code} Client Error: {reason} for url: {response.url}. response: {response.text}"
            )

        elif 500 <= response.status_code < 600:
            http_error_msg = (
                f"{response.status_code} Server Error: {reason} for url: {response.url}. response: {response.text}"
            )

        if http_error_msg:
            raise requests.HTTPError(http_error_msg, response=self)
        

    def _add_page_and_size_to_params(self, page, size , params):
        # Check if params does not contain page or size, if not set it to page and size (or defaults)
        # params dict has precendence over page and size variables
        if not "page" in params.keys():
            params["page"] = page
        if not "size" in params.keys():
            params["size"] = size
        return params

    def request(self, method, url, *args, **kwargs) -> requests.Response:
        logging.debug(f"{method} - {urljoin(self.client_endpoint, url)}")
        if "params" in kwargs:
            logging.debug(f"params: {kwargs['params']}")
        if "json" in kwargs:
            logging.debug(f"Json payload: {json.dumps(kwargs['json'], indent=4)}")
        response = super().request(
            method, urljoin(self.client_endpoint, url), *args, **kwargs
        )
        if response.status_code == 401:
            if (
                "WWW-Authenticate" in response.headers.keys()
                and "invalid_token" in response.headers["WWW-Authenticate"]
            ):
                logging.warning("ContentGrid authorization token expired.")
                if self.has_service_account:
                    logging.debug("Refreshing token...")
                    self.headers["Authorization"] = (
                        f"Bearer {get_application_token(auth_uri=self.auth_uri, client_id=self.client_id, client_secret=self.client_secret)}"
                    )
                    response = super().request(
                        method, urljoin(self.client_endpoint, url), *args, **kwargs
                    )
                else:
                    raise Unauthorized("Token invalid!")
        return response
    
    def follow_link(self, link: "HALLink", expect_json: bool = True, infer_type: type=HALResponse, params={}) -> HALResponse | str:
        response = self.get(link.uri, params=params)
        if expect_json:
            if issubclass(infer_type, InteractiveHALResponse):
                return infer_type(self._validate_json_response(response=response), client=self)
            return infer_type(self._validate_json_response(response=response))
        else:
            self._validate_non_json_response(response=response)
            return response.content
        
    def get_method_from_string(self, http_method:str):
        method_dict = {
            "GET" : self.get,
            "POST" : self.post,
            "PATCH" : self.patch,
            "DELETE" : self.delete,
            "PUT" : self.put
        }
        if http_method not in method_dict.keys():
            raise Exception(f"Unkown method from HAL-forms: {http_method}")
        return method_dict[http_method]