from exchange.moderators.base import Moderator


class PassiveModerator(Moderator):
    def rewrite(self, _: type["exchange.exchange.Exchange"]) -> None:  # noqa: F821
        pass
