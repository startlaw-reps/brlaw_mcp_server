from typing import TYPE_CHECKING

from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

if TYPE_CHECKING:
    from collections.abc import Callable
    from typing import ClassVar, Literal, TypeVar

    from selenium.webdriver.remote.webdriver import WebDriver as _Webdriver
    from selenium.webdriver.remote.webelement import WebElement

    _T = TypeVar("_T")


class WebDriver(Chrome):
    """Extends :class:`selenium.webdriver.Chrome`

    Add methods with functionality frequently used in the implemented behaviors."""

    headless: "ClassVar[bool]" = True
    """Defines if the browser will run in headless mode.

    It should be equal to True in production environments, but it can be set to False for
    debugging purposes."""

    def __init__(self) -> None:
        opts = ChromeOptions()

        args = [
            "--no-sandbox",
            "--disable-dev-shm-usage",
            "user-agent=Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:136.0) Gecko/20100101 Firefox/136.0",
        ] + (["--headless"] if self.headless else [])

        for arg in args:
            opts.add_argument(arg)  # pyright: ignore[reportUnknownMemberType]

        super().__init__(options=opts)

    def wait(
        self,
        condition: "Callable[[_Webdriver], Literal[False] | _T]",
        timeout: int = 10,
    ) -> "_T":
        """Repeatedly invokes the condition until the object returned by it is not false.
        :param condition: Callable that receives this webdriver instance and returns either if the
            condition is satisfied or not.
        :param timeout: Maximum time that will be waited for the condition to be satisfied.
        :return: The object returned by the condition.
        :raise selenium.common.exceptions.TimeoutException: When the condition is not satisfied
            within the maximum time."""
        wait = WebDriverWait(self, timeout)
        return wait.until(condition)

    def wait_for_element_to_be_visible(
        self, css_selector: str, timeout: int = 10
    ) -> "WebElement":
        """Interrupts execution until either the element becomes visible or the timeout elapses.
        :param css_selector: CSS selector to locate the element.
        :param timeout: Maximum time that will be waited for the condition to be satisfied.
        :return: The element that satisfied the condition.
        :raise selenium.common.exceptions.TimeoutException: When the condition is not satisfied
            within the maximum time.
        """
        return self.wait(
            expected_conditions.visibility_of_element_located(
                (By.CSS_SELECTOR, css_selector)
            ),
            timeout,
        )

    def wait_for_element_to_be_invisible(
        self, css_selector: str, timeout: int = 10
    ) -> "WebElement | bool":
        """Interrupts execution until either the element becomes invisible or the timeout elapses.
        :param css_selector: CSS selector to locate the element.
        :param timeout: Maximum time that will be waited for the condition to be satisfied.
        :return: The element, if it exists and is invisible. :class:`True`, if the element does not
            exist.
        :raise selenium.common.exceptions.TimeoutException: If the element exists and does not
            become invisible within the maximum time."""
        return self.wait(
            expected_conditions.invisibility_of_element_located(
                (By.CSS_SELECTOR, css_selector)
            ),
            timeout,
        )

    def wait_for_element_to_be_clickable(
        self, css_selector: str, timeout: int = 10
    ) -> "WebElement":
        """Interrupts execution until either the element becomes clickable or the timeout elapses.
        :param css_selector: CSS selector to locate the element.
        :param timeout: Maximum time that will be waited for the condition to be satisfied.
        :return: The element that satisfied the condition.
        :raise selenium.common.exceptions.TimeoutException: When the condition is not satisfied
            within the maximum time."""
        return self.wait(
            expected_conditions.element_to_be_clickable(
                (By.CSS_SELECTOR, css_selector)
            ),
            timeout,
        )
