"""Domain SearchTweetsTask class."""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from ..model.language import Language


@dataclass(frozen=True)
class SearchTweetsTask:
    """Domain SearchTweetsTask class."""

    all_words: Optional[str]
    exact_words: Optional[str]
    any_word: Optional[str]
    from_username: Optional[str]
    to_username: Optional[str]
    since: Optional[datetime]
    until: Optional[datetime]
    language: Optional[Language]
    verified_user: bool
    tweets_count: Optional[int]

    def __init__(
            self,
            all_words: Optional[str] = None,
            exact_words: Optional[str] = None,
            any_word: Optional[str] = None,
            from_username: Optional[str] = None,
            to_username: Optional[str] = None,
            since: Optional[datetime] = None,
            until: Optional[datetime] = None,
            language: Optional[Language] = None,
            tweets_count: Optional[int] = None
    ):
        """Class constructor."""
        object.__setattr__(self, 'all_words', all_words)
        object.__setattr__(self, 'exact_words', exact_words)
        object.__setattr__(self, 'any_word', any_word)
        object.__setattr__(self, 'from_username', from_username)
        object.__setattr__(self, 'to_username', to_username)
        object.__setattr__(self, 'since', since)
        object.__setattr__(self, 'until', until)
        object.__setattr__(self, 'language', language)
        object.__setattr__(self, 'tweets_count', tweets_count)
        return

    def get_full_search_query(self) -> str:
        """Method to return full search query. This will be contains many details from task, conditions from Twint."""
        query = ''
        if self.all_words is not None:
            query += self.all_words
        if self.exact_words is not None:
            query += '"{}"'.format(self.exact_words)
        if self.any_word is not None:
            query += '({})'.format(" OR ".join(self.any_word.split(" ")))
        if self.language is not None:
            query += f' lang:{self.language.short_value}'
        if self.from_username:
            query += f' from:{self.from_username}'
        if self.since is not None:
            query += f" since:{self._format_date(self.since)}"
        if self.until is not None:
            query += f" until:{self._format_date(self.until)}"
        # if self.verified_user is True:
        #     query += " filter:verified"
        if self.to_username:
            query += f" to:{self.to_username}"
        # if config.Replies:
        #     q += " filter:replies"
        #     # although this filter can still be used, but I found it broken in my preliminary
        #     # testing, needs more testing
        # if config.Native_retweets:
        #     q += " filter:nativeretweets"
        # if config.Min_likes:
        #     q += f" min_faves:{config.Min_likes}"
        # if config.Min_retweets:
        #     q += f" min_retweets:{config.Min_retweets}"
        # if config.Min_replies:
        #     q += f" min_replies:{config.Min_replies}"
        # if config.Links == "include":
        #     q += " filter:links"
        # elif config.Links == "exclude":
        #     q += " exclude:links"
        # if config.Source:
        #     q += f" source:\"{config.Source}\""
        # if config.Members_list:
        #     q += f" list:{config.Members_list}"
        # if config.Filter_retweets:
        #     q += f" exclude:nativeretweets exclude:retweets"
        # if config.Custom_query:
        #     q = config.Custom_query
        return query

    @staticmethod
    def _format_date(date) -> int:
        return int(datetime.strptime(str(date), "%Y-%m-%d %H:%M:%S").timestamp())
