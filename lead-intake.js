/* ============================================================
   lead-intake.js — shared form → BrandOS leads-system handler
   ------------------------------------------------------------
   A form opts in by declaring:
     <form data-lead-source="workshop" data-lead-interest="סדנת World Builder">
   …and including a honeypot field named "lead_hp".
   Submissions are sent to the leads system (agent_leads) and
   trigger a Telegram ping to Hagit. No page reload.
   ============================================================ */
(function () {
  "use strict";

  var ENDPOINT = "https://brandos.hagitantebi.co.il/api/lead-intake";
  var WA_FALLBACK = "https://wa.me/972528351676";

  var NAME_FIELDS = ["name", "full_name", "fullname", "contact_name"];
  var SKIP_FIELDS = ["lead_hp", "_gotcha", "_subject", "_language", "terms"];

  function clean(s) {
    return (s || "").replace(/\s+/g, " ").replace(/\*/g, "").trim();
  }

  // Visible label for a field's group / question.
  function labelText(el) {
    var form = el.form;
    if (el.id && form) {
      var l = form.querySelector('label[for="' + el.id + '"]');
      if (l) return clean(l.textContent);
    }
    var wrap = el.closest(".field, .form-group, .form__group");
    if (wrap) {
      var wl = wrap.querySelector("label");
      if (wl) return clean(wl.textContent);
    }
    var p = el.previousElementSibling;
    while (p) {
      if (p.tagName === "LABEL") return clean(p.textContent);
      p = p.previousElementSibling;
    }
    return el.name || "";
  }

  // Visible label for a single checkbox/radio option.
  function optionLabel(el) {
    if (el.id && el.form) {
      var l = el.form.querySelector('label[for="' + el.id + '"]');
      if (l) return clean(l.textContent);
    }
    if (el.parentElement && el.parentElement.tagName === "LABEL") {
      return clean(el.parentElement.textContent);
    }
    var sib = el.nextElementSibling;
    if (sib && sib.tagName === "LABEL") return clean(sib.textContent);
    return el.value;
  }

  function collect(form) {
    var name = "";
    var email = "";
    var phone = "";
    var lines = [];
    var seenGroups = {};
    var els = form.elements;

    for (var i = 0; i < els.length; i++) {
      var el = els[i];
      if (!el.name || SKIP_FIELDS.indexOf(el.name) !== -1) continue;
      var type = (el.type || "").toLowerCase();
      if (type === "submit" || type === "button" || type === "hidden") continue;

      if (NAME_FIELDS.indexOf(el.name) !== -1 && !name) {
        name = el.value.trim();
      }
      if (type === "email" && !email && el.value.trim()) {
        email = el.value.trim();
      }
      if (
        (type === "tel" || el.name === "phone" || el.name === "tel") &&
        !phone &&
        el.value.trim()
      ) {
        phone = el.value.trim();
      }

      if (type === "checkbox" || type === "radio") {
        if (seenGroups[el.name]) continue;
        seenGroups[el.name] = true;
        var picked = [];
        var group = form.querySelectorAll('[name="' + el.name + '"]');
        for (var g = 0; g < group.length; g++) {
          if (group[g].checked) picked.push(optionLabel(group[g]));
        }
        if (picked.length) {
          lines.push(labelText(el) + ": " + picked.join(", "));
        }
        continue;
      }

      var v;
      if (el.tagName === "SELECT") {
        v =
          el.value && el.selectedIndex >= 0
            ? clean(el.options[el.selectedIndex].text)
            : "";
      } else {
        v = (el.value || "").trim();
      }
      if (v) lines.push(labelText(el) + ": " + v);
    }

    return {
      name: name,
      contact: phone || email,
      contactType: phone ? "phone" : "email",
      summary: lines.join("\n"),
    };
  }

  function showSuccess(form) {
    var box = document.createElement("div");
    box.setAttribute("dir", "rtl");
    box.style.cssText = "text-align:center;padding:48px 24px;font-family:inherit;";
    box.innerHTML =
      '<div style="font-size:2.75rem;line-height:1;margin-bottom:14px;color:#C28A5A;">✓</div>' +
      '<h3 style="font-size:1.5rem;margin:0 0 8px;font-weight:600;">תודה!</h3>' +
      '<p style="margin:0;opacity:.7;">הפרטים התקבלו. אחזור אליכם בהקדם.</p>';
    form.style.display = "none";
    form.parentNode.insertBefore(box, form.nextSibling);
    try {
      box.scrollIntoView({ behavior: "smooth", block: "center" });
    } catch (e) {}
    // Signal a confirmed lead so pages can fire conversion pixels (e.g. Meta "Lead").
    try {
      document.dispatchEvent(
        new CustomEvent("lead:intake:success", {
          detail: { source: form.dataset.leadSource || "website" },
        })
      );
    } catch (e) {}
  }

  function showError(form, msg) {
    var box = form.querySelector(".lead-intake-error");
    if (!box) {
      box = document.createElement("p");
      box.className = "lead-intake-error";
      box.style.cssText =
        "margin-top:14px;text-align:center;color:#b4452f;font-size:.9rem;";
      form.appendChild(box);
    }
    box.innerHTML =
      msg +
      ' — או פנו ישירות ב<a href="' +
      WA_FALLBACK +
      '" target="_blank" rel="noopener" style="color:inherit;">וואטסאפ</a>.';
  }

  function handle(form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();

      var data = collect(form);
      if (!data.contact) {
        showError(form, "צריך למלא טלפון או אימייל");
        return;
      }

      var btn = form.querySelector('[type="submit"]');
      var hp = form.querySelector('[name="lead_hp"]');
      if (btn) {
        btn.disabled = true;
        btn.style.opacity = "0.6";
      }

      var payload = {
        source: form.dataset.leadSource || "website",
        interest: form.dataset.leadInterest || "",
        name: data.name,
        contact: data.contact,
        contact_type: data.contactType,
        summary: data.summary,
        hp: hp ? hp.value : "",
      };

      fetch(ENDPOINT, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      })
        .then(function (res) {
          if (!res.ok) throw new Error("bad status");
          return res.json();
        })
        .then(function () {
          showSuccess(form);
        })
        .catch(function () {
          if (btn) {
            btn.disabled = false;
            btn.style.opacity = "";
          }
          showError(form, "השליחה נכשלה");
        });
    });
  }

  function init() {
    var forms = document.querySelectorAll("form[data-lead-source]");
    for (var i = 0; i < forms.length; i++) handle(forms[i]);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
