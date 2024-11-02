from __future__ import annotations

import contextlib
import typing
from typing import Literal, overload

from bs4 import BeautifulSoup
from bs4.element import ResultSet, Tag
from httpx._models import Response

from .broadcast_list import TagBroadcastList
from .exceptions import EmptyResultError

T = typing.TypeVar("T")


@typing.overload
def _resolve_default(*args: T | None, allow_none: typing.Literal[False] = ...) -> T:
    ...


@typing.overload
def _resolve_default(*args: T, allow_none: typing.Literal[True] = ...) -> T:
    ...


@typing.overload
def _resolve_default(*args: T, allow_none: bool = False) -> T:
    ...


def _resolve_default(*args: T | None, allow_none: bool = False) -> T | None:
    for arg in args:
        if arg is not None:
            return arg
    if allow_none:
        return None
    raise ValueError(
        f"No matched arguments. args: {args}" "This message is provided because allow_none parameter was False."
    )


Parsers = Literal["html.parser", "html", "lxml", "lxml-xml", "xml", "html5lib", "html5"]


class SoupTools:
    def __init__(
        self,
        text: str | None,
        *,
        parser: Parsers | None = None,
        no_empty_result: bool | None = None,
    ) -> None:
        if text is None:
            assert type(self) is not SoupTools, "None in text field is not allowed."
        else:
            self.text: str = text

        self.parser: Parsers | None = parser
        self.no_empty_result = no_empty_result

    def _raise_error(
        self,
        error_message: str,
        selector: str,
        **kwargs,
    ) -> typing.NoReturn:
        raise EmptyResultError(error_message, selector=selector, **kwargs)

    def soup(
        self,
        parser: Parsers | None = None,
    ) -> BeautifulSoup:
        with contextlib.suppress(AttributeError):
            return self._soup_cache

        parser = _resolve_default(parser, self.parser, "html.parser")

        self._soup_cache = BeautifulSoup(self.text, parser)
        return self._soup_cache

    def soup_select(
        self,
        selector: str,
        no_empty_result: bool | None = None,
        parser: Parsers | None = None,
        **kwargs,
    ) -> TagBroadcastList:
        """response.soup(parser, **kwargs).select(selector)와 거의 같습니다만 no_empty_result라는 강력한 추가 기능을 제공합니다.

        Args:
            self (str | Response): markup or response you want to parse.
            selector (str): BeatifulSoup.select의 selector입니다.
            no_empty_result (bool, optional): 결과가 빈 리스트라면 EmptyResultError를 냅니다. Defaults to False.
            parser (Parsers, optional): BeatifulSoup의 parser입니다. Defaults to 'html.parser'.

        Raises:
            EmptyResultError: 결과가 빈 리스트이고 no_empty_result가 참이라면 EmptyResultError를 냅니다.
                결과가 None일때 오류를 내는 것이 아니라는 점을 주의하세요.

        Returns:
            ResultSet[Tag]
        """
        selected = self.soup(parser).select(selector, **kwargs)
        no_empty_result = _resolve_default(no_empty_result, self.no_empty_result, False)
        if no_empty_result and not selected:
            self._raise_error(
                'Selecting result is empty list("[]").',
                selector=selector,
            )

        return TagBroadcastList(selected)

    @overload
    def soup_select_one(
        self,
        selector: str,
        no_empty_result: Literal[False] = ...,
        parser: Parsers | None = None,
        **kwargs,
    ) -> Tag | None:
        ...

    @overload
    def soup_select_one(
        self,
        selector: str,
        no_empty_result: Literal[True] = ...,
        parser: Parsers | None = None,
        **kwargs,
    ) -> Tag:
        ...

    @overload
    def soup_select_one(
        self,
        selector: str,
        no_empty_result: bool | None = None,
        parser: Parsers | None = None,
        **kwargs,
    ) -> Tag | None:
        ...

    def soup_select_one(
        self,
        selector: str,
        no_empty_result: bool | None = None,
        parser: Parsers | None = None,
        **kwargs,
    ) -> Tag | None:
        """response.soup(parser, **kwargs).select_one(selector)와 거의 같습니다만 no_empty_result라는 강력한 추가 기능을 제공합니다.

        Args:
            self (str | Response): markup or response you want to parse.
                (ResponesProxy에서 사용할 경우 없음)
            selector (str): BeatifulSoup.select_one의 selector입니다.
            no_empty_result (bool, optional): 결과(리턴값)가 None라면 EmptyResultError를 냅니다.
                typing과 오류 제거에 상당한 도움을 줍니다. 기존의 BeatifulSoup.select_one의 경우에는
                결과값이 None이거나 Tag였습니다. 따라서 BeatifulSoup.select_one(selector).text와 같은
                코드를 짤 때 정적 타입 검사기에서 오류를 내기 일쑤였고, 실제로 해당 코드 실행 결과가 None일 경우
                오류가 났습니다. no_empty_list를 이용해 불명확한 오류 대신 EmptyResultError를 내보내고
                타입 검사기의 오류도 피할 수 있어 좋은 기능입니다. 하지만 어떠한 이유로든지 이 기능을 사용하고
                싶지 않다면 간단히 그냥 값을 False로 하면 됩니다. Defaults to True.
            parser (Parsers, optional): BeatifulSoup의 parser입니다. Defaults to 'html.parser'.

        Raises:
            EmptyResultError: 결과가 None이고 no_empty_result가 참이라면 EmptyResultError를 냅니다.

        Returns:
            Tag | None: no_empty_result가 False일 경우(기본값)
            Tag: no_empty_result가 True일 경우(정적 검사기에 반영됨)
        """
        select_results = self.soup(parser=parser).select_one(selector, **kwargs)
        no_empty_result = _resolve_default(no_empty_result, self.no_empty_result, False)
        if no_empty_result and select_results is None:
            self._raise_error(
                "Selecting result is None.",
                selector=selector,
            )

        return select_results

    # XML

    def xml(self) -> BeautifulSoup:
        """parser가 xml인 .soup()입니다. 자세한 내용은 .soup()의 docstring을 확인하세요."""
        # functools.partial을 사용할까도 했지만 그러면 type hint와 docstring 사용이 어렵다.
        return self.soup(parser="xml")

    def xml_select(
        self,
        selector: str,
        no_empty_result: bool | None = None,
        **kwargs,
    ) -> TagBroadcastList:
        """parser가 xml인 .soup_select()입니다. 자세한 내용은 .soup_select()의 docstring을 확인하세요."""
        return self.soup_select(selector, no_empty_result, "xml", **kwargs)

    @overload
    def xml_select_one(
        self,
        selector: str,
        no_empty_result: Literal[True] = ...,
        **kwargs,
    ) -> Tag:
        ...

    @overload
    def xml_select_one(
        self,
        selector: str,
        no_empty_result: Literal[True] = ...,
        **kwargs,
    ) -> Tag:
        ...

    @overload
    def xml_select_one(
        self,
        selector: str,
        no_empty_result: bool | None = None,
        **kwargs,
    ) -> Tag | None:
        ...

    def xml_select_one(
        self,
        selector: str,
        no_empty_result: bool | None = None,
        **kwargs,
    ) -> Tag | None:
        """parser가 xml인 .soup_select_one()입니다. 자세한 내용은 .soup_select_one()의 docstring을 확인하세요."""
        return self.soup_select_one(selector, no_empty_result, "xml")


class NotEmptySoupTools(SoupTools):
    def __init__(
        self,
        text: str | None,
        *,
        parser: Parsers | None = None,
    ) -> None:
        if text is None:
            assert type(self) is not SoupTools, "None in text field is not allowed."
        else:
            self.text: str = text

        self.parser: Parsers | None = parser

    def soup_select(
        self,
        selector: str,
        parser: Parsers | None = None,
        **kwargs,
    ) -> TagBroadcastList:
        return super().soup_select(selector, no_empty_result=True, parser=parser, **kwargs)

    def soup_select_one(
        self,
        selector: str,
        parser: Parsers | None = None,
        **kwargs,
    ) -> Tag:
        return super().soup_select_one(selector, no_empty_result=True, parser=parser, **kwargs)

    # XML

    def xml_select(
        self,
        selector: str,
        **kwargs,
    ) -> TagBroadcastList:
        """parser가 xml인 .soup_select()입니다. 자세한 내용은 .soup_select()의 docstring을 확인하세요."""
        return super().soup_select(selector, no_empty_result=True, parser="xml", **kwargs)

    def xml_select_one(
        self,
        selector: str,
        **kwargs,
    ) -> Tag:
        """parser가 xml인 .soup_select_one()입니다. 자세한 내용은 .soup_select_one()의 docstring을 확인하세요."""
        return self.soup_select_one(selector, "xml", **kwargs)


class SoupedResponse(Response, SoupTools):
    def __init__(
        self,
        response: Response,
        *,
        parser: Parsers | None = None,
        no_empty_result: bool | None = None,
    ) -> None:
        self.__dict__ = response.__dict__
        super(Response, self).__init__(
            None,
            parser=parser,
            no_empty_result=no_empty_result,
        )

    def _raise_error(self, *args, **kwargs):
        super()._raise_error(
            *args,
            **kwargs,
            url=self.url,
            status_code=self.status_code,
        )


class NotEmptySoupedResponse(SoupedResponse, NotEmptySoupTools):
    def __init__(
        self,
        response: Response,
        *,
        parser: Parsers | None = None,
        no_empty_result: bool | None = None,
    ) -> None:
        self.__dict__ = response.__dict__
        super(NotEmptySoupTools, self).__init__(
            None,
            parser=parser,
            no_empty_result=no_empty_result,
        )
