(() => {
  const $ = (s, el = document) => el.querySelector(s);
  const $$ = (s, el = document) => [...el.querySelectorAll(s)];
  const fmt = (n) => Math.round(n).toLocaleString("sv-SE").replace(/\s/g, " ") + " kr";

  /* ------------------------------------------------ header */
  const siteHeader = $(".site-header");
  const nav = $("#nav");
  const menuBtn = $(".menu-btn");
  let menuOpen = false;
  const syncHeader = () => siteHeader.classList.toggle("is-solid", menuOpen || window.scrollY > 40);
  window.addEventListener("scroll", syncHeader, { passive: true });
  syncHeader();

  menuBtn?.addEventListener("click", () => {
    menuOpen = menuBtn.getAttribute("aria-expanded") !== "true";
    menuBtn.setAttribute("aria-expanded", menuOpen);
    nav.classList.toggle("open", menuOpen);
    document.body.style.overflow = menuOpen ? "hidden" : "";
    syncHeader();
  });
  const closeMenu = () => {
    menuOpen = false;
    menuBtn?.setAttribute("aria-expanded", "false");
    nav?.classList.remove("open");
    document.body.style.overflow = "";
    syncHeader();
  };
  $$(".nav a").forEach((a) => a.addEventListener("click", closeMenu));

  $$(".has-sub").forEach((li) => {
    const btn = $(".nav-sub-toggle", li);
    const set = (open) => { li.classList.toggle("open", open); btn.setAttribute("aria-expanded", open); };
    btn.addEventListener("click", (ev) => { ev.stopPropagation(); set(!li.classList.contains("open")); });
    document.addEventListener("click", (ev) => { if (!li.contains(ev.target)) set(false); });
    document.addEventListener("keydown", (ev) => { if (ev.key === "Escape") set(false); });
  });

  /* ------------------------------------------------ mobile call/quote bar */
  const bar = $(".mobile-bar");
  const offer = $("#offert");
  if (bar) {
    let offerVisible = false;
    if (offer && "IntersectionObserver" in window) {
      new IntersectionObserver(([en]) => { offerVisible = en.isIntersecting; update(); }).observe(offer);
    }
    function update() { bar.classList.toggle("show", window.scrollY > 420 && !offerVisible); }
    window.addEventListener("scroll", update, { passive: true });
    update();
  }

  /* ------------------------------------------------ quote form */
  const forms = $$("[data-quote-form]");

  function prefill(opts) {
    const form = offer?.matches("[data-quote-form]") ? offer : offer?.querySelector("[data-quote-form]") || forms[0];
    if (!form) return;
    if (opts.service) {
      const opt = $$("option", form.tjanst).find((o) => o.dataset.slug === opts.service);
      if (opt) { form.tjanst.value = opt.value; form.tjanst.dispatchEvent(new Event("change")); }
    }
    if (opts.kvm) form.kvm.value = opts.kvm;
    if (opts.note && !form.meddelande.value) form.meddelande.value = opts.note;
  }

  document.addEventListener("click", (ev) => {
    const a = ev.target.closest("[data-quote]");
    if (!a) return;
    if (!offer) { ev.preventDefault(); location.href = "/karrahemstad/preview/#offert"; return; }
    if (a.dataset.service) prefill({ service: a.dataset.service });
  });

  forms.forEach((form) => {
    form.classList.add("js-ready");
    const label = $("[data-step-label]", form);
    const err = $("[data-error]", form);
    const propMap = JSON.parse($("[data-prop-map]", form).textContent);
    const allProps = $$("option", form.lokal).map((o) => o.value);

    const goStep = (n) => {
      form.classList.toggle("is-step-2", n === 2);
      label.textContent = `Steg ${n} av 2`;
      const first = $(`[data-step="${n}"] input, [data-step="${n}"] select`, form);
      first?.focus({ preventScroll: true });
      const top = form.getBoundingClientRect().top;
      if (top < 0) form.scrollIntoView({ block: "start" });
    };

    form.tjanst.addEventListener("change", () => {
      const slug = form.tjanst.selectedOptions[0].dataset.slug;
      const list = propMap[slug] || allProps;
      const cur = form.lokal.value;
      form.lokal.innerHTML = list.map((p) => `<option${p === cur ? " selected" : ""}>${p}</option>`).join("");
    });

    $("[data-next]", form).addEventListener("click", () => goStep(2));
    $("[data-back]", form).addEventListener("click", () => goStep(1));

    form.addEventListener("submit", async (ev) => {
      ev.preventDefault();
      err.hidden = true;
      const required = [form.namn, form.telefon];
      required.forEach((f) => f.setAttribute("aria-invalid", !f.value.trim()));
      const missing = required.find((f) => !f.value.trim());
      if (missing) { err.textContent = "Fyll i namn och telefonnummer så att vi kan nå dig."; err.hidden = false; missing.focus(); return; }
      if (form._gotcha.value) return;

      const data = Object.fromEntries(new FormData(form));
      delete data._gotcha;
      const btn = $("button[type=submit]", form);
      btn.disabled = true;

      const endpoint = form.dataset.endpoint;
      try {
        if (endpoint) {
          const res = await fetch(endpoint, {
            method: "POST",
            headers: { "Content-Type": "application/json", Accept: "application/json" },
            body: JSON.stringify({ ...data, _subject: `Offertförfrågan: ${data.tjanst}`, sida: location.pathname }),
          });
          if (!res.ok) throw new Error(res.status);
        } else {
          const lines = [
            ["Tjänst", data.tjanst], ["Typ av lokal", data.lokal], ["Storlek (kvm)", data.kvm],
            ["Postnummer/ort", data.ort], ["Önskat datum", data.datum], ["Namn", data.namn],
            ["Telefon", data.telefon], ["E-post", data.epost], ["Meddelande", data.meddelande],
          ].filter(([, v]) => v).map(([k, v]) => `${k}: ${v}`);
          location.href = `mailto:${form.dataset.email}?subject=${encodeURIComponent("Offertförfrågan: " + data.tjanst)}&body=${encodeURIComponent(lines.join("\n"))}`;
        }
        form.classList.add("is-done");
        const done = $("[data-done]", form);
        done.hidden = false;
        done.focus();
      } catch (e) {
        err.textContent = "Något gick fel. Försök igen eller ring oss på 031-27 89 98.";
        err.hidden = false;
      } finally {
        btn.disabled = false;
      }
    });
  });

  /* ------------------------------------------------ price calculator */
  $$("[data-calc]").forEach((calc) => {
    const services = JSON.parse($("[data-calc-data]", calc).textContent);
    const sel = $("[data-calc-service]", calc);
    const range = $("[data-calc-range]", calc);
    const num = $("[data-calc-number]", calc);
    const unit = $("[data-calc-unit]", calc);
    const amountLabel = $("[data-calc-amount-label]", calc);
    const total = $("[data-calc-total]", calc);
    const note = $("[data-calc-note]", calc);
    const cta = $("[data-calc-cta]", calc);
    const state = { mode: "kvm", kvm: 70, hour: 3 };

    const fillServices = () => {
      const cur = sel.value;
      const list = services.filter((s) => s[state.mode]);
      sel.innerHTML = list.map((s) => `<option value="${s.slug}">${s.name}</option>`).join("");
      if (list.some((s) => s.slug === cur)) sel.value = cur;
    };

    const render = () => {
      const s = services.find((x) => x.slug === sel.value);
      const amount = state[state.mode];
      const sum = s[state.mode] * amount;
      total.textContent = fmt(sum);
      note.textContent = s.business
        ? `ex. moms · ${s[state.mode]} kr/${state.mode === "kvm" ? "kvm" : "h"}`
        : `efter RUT, inkl. moms och material · ${s[state.mode]} kr/${state.mode === "kvm" ? "kvm" : "h"}`;
      cta.dataset.service = s.slug;
      cta.dataset.amount = amount;
      cta.dataset.sum = sum;
    };

    const setMode = (mode) => {
      state.mode = mode;
      const kvm = mode === "kvm";
      range.min = kvm ? 20 : 1;
      range.max = kvm ? 250 : 8;
      range.step = kvm ? 5 : 1;
      range.value = num.value = state[mode];
      unit.textContent = kvm ? "kvm" : "tim";
      amountLabel.textContent = kvm ? "Bostadens storlek" : "Antal timmar";
      fillServices();
      render();
    };

    $$("input[name=calc-mode]", calc).forEach((r) => r.addEventListener("change", () => setMode(r.value)));
    sel.addEventListener("change", render);
    range.addEventListener("input", () => { state[state.mode] = +range.value; num.value = range.value; render(); });
    num.addEventListener("input", () => {
      const v = Math.max(0, Math.min(9999, parseInt(num.value, 10) || 0));
      state[state.mode] = v;
      range.value = v;
      render();
    });

    cta.addEventListener("click", () => {
      const s = services.find((x) => x.slug === sel.value);
      const u = state.mode === "kvm" ? "kvm" : "timmar";
      prefill({
        service: s.slug,
        kvm: state.mode === "kvm" ? state.kvm : "",
        note: `Uträknat på sajten: ${s.name}, ${state[state.mode]} ${u} ≈ ${fmt(+cta.dataset.sum).replace(/ /g, " ")}.`,
      });
    });

    setMode("kvm");
  });
})();
