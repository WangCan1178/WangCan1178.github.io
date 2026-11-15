(function () {
  var STORAGE_KEY = "site-lang";

  function currentLang() {
    return document.documentElement.classList.contains("lang-zh") ? "zh" : "en";
  }

  function applyChrome(lang) {
    document.documentElement.lang = lang === "zh" ? "zh-CN" : "en";

    document.querySelectorAll("[data-set-lang]").forEach(function (button) {
      var active = button.getAttribute("data-set-lang") === lang;
      button.setAttribute("aria-pressed", active ? "true" : "false");
    });

    var searchInput = document.getElementById("bibsearch");
    if (searchInput) {
      searchInput.placeholder =
        lang === "zh"
          ? searchInput.getAttribute("data-placeholder-zh") || "输入以筛选"
          : searchInput.getAttribute("data-placeholder-en") || "Type to filter";
    }

    document.querySelectorAll(".more-authors").forEach(function (element) {
      if (element.getAttribute("data-expanded") === "true") return;
      element.title = lang === "zh" ? "点击查看其余作者" : "click to view more authors";
    });

    var ninjaKeys = document.querySelector("ninja-keys");
    if (ninjaKeys) {
      var searchPlaceholder = lang === "zh" ? "输入以开始搜索" : "Type to start searching";
      ninjaKeys.placeholder = searchPlaceholder;
      ninjaKeys.setAttribute("placeholder", searchPlaceholder);
    }

    var searchButton = document.getElementById("search-toggle");
    if (searchButton) {
      searchButton.title = lang === "zh" ? "搜索" : "Search";
      searchButton.setAttribute("aria-label", lang === "zh" ? "打开搜索" : "Open search");
    }

    var themeButton = document.getElementById("light-toggle");
    if (themeButton) {
      var themeLabel = lang === "zh" ? "切换颜色主题" : "Change color theme";
      themeButton.title = themeLabel;
      themeButton.setAttribute("aria-label", themeLabel);
    }

    var navButton = document.querySelector(".navbar-toggler-main");
    if (navButton) {
      navButton.setAttribute("aria-label", lang === "zh" ? "展开导航" : "Toggle navigation");
    }

    var titleZh = document.documentElement.getAttribute("data-title-zh");
    if (!document.documentElement.dataset.titleEn) {
      document.documentElement.dataset.titleEn = document.title;
    }
    if (lang === "zh" && titleZh) {
      var path = window.location.pathname;
      document.title = path === "/" || path === "" ? titleZh : titleZh + " | 王灿";
    } else {
      document.title = document.documentElement.dataset.titleEn;
    }
  }

  function setLang(lang) {
    document.documentElement.classList.toggle("lang-zh", lang === "zh");
    try {
      localStorage.setItem(STORAGE_KEY, lang);
    } catch (error) {}
    applyChrome(lang);
  }

  document.addEventListener("click", function (event) {
    var langButton = event.target.closest("[data-set-lang]");
    if (langButton) {
      setLang(langButton.getAttribute("data-set-lang"));
      return;
    }

    var moreAuthors = event.target.closest(".more-authors");
    if (!moreAuthors || !moreAuthors.dataset.show) return;

    if (moreAuthors.getAttribute("data-expanded") === "true") {
      moreAuthors.innerHTML =
        '<span class="lang-only" data-lang="en"></span><span class="lang-only" data-lang="zh"></span>';
      moreAuthors.querySelector('[data-lang="en"]').textContent = moreAuthors.dataset.hideEn;
      moreAuthors.querySelector('[data-lang="zh"]').textContent = moreAuthors.dataset.hideZh;
      moreAuthors.setAttribute("data-expanded", "false");
      moreAuthors.title = currentLang() === "zh" ? "点击查看其余作者" : "click to view more authors";
    } else {
      moreAuthors.innerHTML = moreAuthors.dataset.show;
      moreAuthors.setAttribute("data-expanded", "true");
      moreAuthors.title = "";
    }
  });

  applyChrome(currentLang());
})();
