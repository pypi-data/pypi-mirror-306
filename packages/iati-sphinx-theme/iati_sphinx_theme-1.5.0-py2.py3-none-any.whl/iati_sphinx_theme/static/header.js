(function () {
  /**
   * @param {Object} container DOM element, which will be hidden\displayed (required)
   * @param {string} options the class to be toggled.
   */
  class IatiMobileNav {
    constructor(wrapper, openClass) {
      this.wrapper = wrapper;
      this.openClass = openClass;
      const focusableElements = this.wrapper.querySelectorAll("a, button");
      this.firstElement = focusableElements[0];
      this.lastElement = focusableElements[focusableElements.length - 1];
    }

    show = () => {
      this.wrapper.removeAttribute("hidden");
      const reflow = this.wrapper.offsetHeight;
      document.addEventListener("keydown", (e) => this.handleKeyDown(e));
      this.wrapper.classList.add(this.openClass);
      setTimeout(() => {
        this.firstElement.focus();
      }, 500);
    };

    hide = (closeCallBack) => {
      this.wrapper.classList.remove(this.openClass);
      document.removeEventListener("keydown", (e) => this.handleKeyDown(e));
      setTimeout(() => {
        this.wrapper.setAttribute("hidden", "hidden");
        closeCallBack();
      }, 500);
    };

    handleKeyDown(event) {
      if (event.key === "Tab") {
        if (document.activeElement === this.firstElement && event.shiftKey) {
          this.lastElement.focus();
          event.preventDefault();
        }
        if (document.activeElement === this.lastElement && !event.shiftKey) {
          this.firstElement.focus();
          event.preventDefault();
        }
      }
      if (event.key == "Escape") {
        this.hide();
      }
    }
  }

  document.addEventListener("DOMContentLoaded", function () {
    const iatiMobileNav = new IatiMobileNav(
      document.querySelector(".js-iati-mobile-nav"),
      "iati-mobile-nav--open"
    );

    const overlay = document.querySelector(".js-iati-mobile-overlay");
    const menuOpenBtn = document.querySelector(".js-iati-menu-toggle-open");
    const menuCloseBtn = document.querySelector(".js-iati-menu-toggle-close");
    const restoreFocus = () => {
      menuOpenBtn.focus();
    };
    menuOpenBtn.addEventListener("click", iatiMobileNav.show);
    menuCloseBtn.addEventListener("click", () =>
      iatiMobileNav.hide(restoreFocus)
    );
    overlay.addEventListener("click", () => iatiMobileNav.hide(restoreFocus));
  });
})();
