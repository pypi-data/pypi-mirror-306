from requests import Session
from typing import Union


class Network(object):
    """UniFi Network controller class"""

    def __init__(self, controller: str, username: str, password: str, site: str = "default"):
        self._session = Session()
        self._controller = controller
        resp = self._session.post(
            f"https://{controller}/api/login",
            headers={"Content-Type": "application/json"},
            json={"username": username, "password": password},
            verify=False,
        )
        resp.raise_for_status()
        if site != "default":
            self._set_site(site)
        else:
            self._site = site

    @property
    def site(self):
        return self._site

    def _set_site(self, site_descr: str) -> None:
        """Get the name (ID) for a site given its description."""
        resp = self._session.get(f"https://{self._controller}/api/self/sites", verify=False)
        resp.raise_for_status()

        site_list = resp.json()
        if site_list["meta"]["rc"] == "ok":
            for site in site_list["data"]:
                if site["desc"] == site_descr:
                    self._site = site["name"]
                    return

        raise Exception(f"Failed to set site to {site_descr}")

    def get_devices(self) -> list[dict]:
        """Get a list of devices and their details."""
        resp = self._session.get(
            f"https://{self._controller}/api/s/{self._site}/stat/device",
            verify=False,
        )
        resp.raise_for_status()

        dev_list = resp.json()
        if dev_list["meta"]["rc"] == "ok":
            return dev_list["data"]
        else:
            raise Exception("Error obtaining device list")

    def get_health(self) -> list:
        """Get the overall network health from the controller"""
        resp = self._session.get(f"https://{self._controller}/api/s/{self._site}/stat/health", verify=False)
        resp.raise_for_status()

        return resp.json()["data"]

    def get_networks(self) -> list:
        """Get a list of networks from the controller"""
        resp = self._session.get(f"https://{self._controller}/api/s/{self._site}/rest/networkconf", verify=False)
        resp.raise_for_status()

        network_list = resp.json()
        if network_list["meta"]["rc"] == "ok":
            return network_list["data"]

        raise Exception(f"Failed to get network list (status: {network_list['meta']['rc']})")

    def add_network(self, **kwargs) -> dict:
        """Add a wired network to the controller"""
        resp = self._session.post(f"https://{self._controller}/api/s/{self._site}/rest/networkconf", verify=False, json=kwargs)
        resp.raise_for_status()
        j = resp.json()
        if j["meta"]["rc"] == "ok":
            return j["data"][0]

        raise Exception(f"Failed to create new network on UniFi (status: {j['meta']['rc']})")

    def remove_network(self, nid: str) -> None:
        """Remove a network from the UniFi controller"""
        resp = self._session.delete(f"https://{self._controller}/api/s/{self._site}/rest/networkconf/{nid}", verify=False)
        resp.raise_for_status()
        j = resp.json()
        if j["meta"]["rc"] != "ok":
            raise Exception(f"Failed to delete network from UniFi (status: {j['meta']['rc']})")

    def add_profile(self, **kwargs) -> dict:
        """Add a port profile to the controller"""
        resp = self._session.post(f"https://{self._controller}/api/s/{self._site}/rest/portconf", verify=False, json=kwargs)
        resp.raise_for_status()
        j = resp.json()
        if j["meta"]["rc"] == "ok":
            return j["data"][0]

        raise Exception(f"Failed to create new port profile on UniFi (status: {j['meta']['rc']})")

    def get_active_clients(self) -> list:
        """Get the current list of active clients from the controller"""
        resp = self._session.get(f"https://{self._controller}/v2/api/site/{self._site}/clients/active", verify=False)
        resp.raise_for_status()
        return resp.json()

    def forget_devices(self, device: Union[list, str]) -> None:
        """Forget a device or list of devices"""
        devices = device
        if isinstance(device, str):
            devices = [device]

        resp = self._session.post(
            f"https://{self._controller}/api/s/{self._site}/cmd/sitemgr", json={"macs": devices, "cmd": "delete-device"}, verify=False
        )
        resp.raise_for_status()
        j = resp.json()
        if j["meta"]["rc"] == "ok":
            return

        raise Exception(f"Failed to forget device(s) on the controller (status: {j['meta']['rc']})")
