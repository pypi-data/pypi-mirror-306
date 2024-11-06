from typing import Dict, Optional, Type, cast

from .interface import OutletInterface


class AP790XOutlet(OutletInterface):
    def __init__(
        self,
        *,
        host: str,
        outlet: int,
        read_community: str = "public",
        write_community: str = "private",
    ) -> None:
        if outlet < 1 or outlet > 8:
            raise Exception("Out of bounds outlet number!")

        # Import this here to pay less cost to speed of startup.
        from .snmp import SNMPOutlet

        self.host = host
        self.outlet = outlet
        self.read_community = read_community
        self.write_community = write_community
        self.snmp = SNMPOutlet(
            host=host,
            query_oid=f"1.3.6.1.4.1.318.1.1.12.3.3.1.1.4.{outlet}",
            query_on_value=1,
            query_off_value=2,
            update_oid=f"1.3.6.1.4.1.318.1.1.12.3.3.1.1.4.{outlet}",
            update_on_value=1,
            update_off_value=2,
            read_community=read_community,
            write_community=write_community,
        )

    def serialize(self) -> Dict[str, object]:
        return {
            "host": self.host,
            "outlet": self.outlet,
            "read_community": self.read_community,
            "write_community": self.write_community,
        }

    @classmethod
    def deserialize(
        cls: "Type[AP790XOutlet]", vals: Dict[str, object]
    ) -> "AP790XOutlet":
        return cls(
            host=cast(str, vals["host"]),
            outlet=cast(int, vals["outlet"]),
            read_community=cast(str, vals["read_community"]),
            write_community=cast(str, vals["write_community"]),
        )

    def getState(self) -> Optional[bool]:
        return self.snmp.getState()

    def setState(self, state: bool) -> None:
        return self.snmp.setState(state)
