/* SEKAI Board — tema, helpers y páginas */
(function () {
  const html = document.documentElement;

  function applyTheme(t) {
    html.setAttribute("data-bs-theme", t);
    localStorage.setItem("sekai-theme", t);
    const btn = document.getElementById("themeToggle");
    if (btn) btn.innerHTML = t === "dark" ? "☀️" : "🌙";
  }

  document.addEventListener("DOMContentLoaded", function () {
    applyTheme(html.getAttribute("data-bs-theme") || "dark");
    const btn = document.getElementById("themeToggle");
    if (btn) btn.addEventListener("click", function () {
      applyTheme(html.getAttribute("data-bs-theme") === "dark" ? "light" : "dark");
    });
    // nav activa según data-page
    const page = document.body.dataset.page;
    if (page) {
      const link = document.querySelector('.nav-link[data-nav="' + page + '"]');
      if (link) link.classList.add("active");
    }
    if (window.SEKAI && typeof renderPage === "function") renderPage(window.SEKAI);
  });

  // ---------- helpers ----------
  window.fmtDate = function (ms) {
    if (!ms) return "";
    return new Date(ms).toLocaleDateString("es-BO", { day: "numeric", month: "short", year: "numeric" });
  };
  window.esc = function (s) {
    return String(s).replace(/[&<>"]/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
  };
  window.unitColor = function (unitId) {
    const u = (window.SEKAI?.units || []).find(u => u.id === unitId);
    return u ? u.color : "var(--sekai-accent)";
  };
  window.unitName = function (unitId) {
    const u = (window.SEKAI?.units || []).find(u => u.id === unitId);
    return u ? u.name : unitId;
  };
  window.attrColor = { warm: "#FFB13D", cute: "#FF8FBA", cool: "#5B8CFF", mysterious: "#A77BFF", pure: "#5FD4E8" };
})();
