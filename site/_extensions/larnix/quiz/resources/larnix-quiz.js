/* Larnix client-side quiz engine.
 *
 * Finds every <div class="larnix-quiz"> containing a JSON quiz (embedded by the
 * `quiz` shortcode), renders the MCQs, scores client-side on submit, shows the
 * correct answers + explanations, and persists the best score in localStorage.
 * No backend, no dependencies.
 */
(function () {
  "use strict";

  function el(tag, cls, text) {
    var e = document.createElement(tag);
    if (cls) e.className = cls;
    if (text != null) e.textContent = text;
    return e;
  }

  function storageKey(id) {
    return "larnix-quiz:" + id;
  }

  function loadProgress(id) {
    try {
      return JSON.parse(localStorage.getItem(storageKey(id)) || "null");
    } catch (e) {
      return null;
    }
  }

  function saveProgress(id, record) {
    try {
      localStorage.setItem(storageKey(id), JSON.stringify(record));
    } catch (e) {
      /* storage may be unavailable (private mode) — scoring still works */
    }
  }

  function renderQuiz(container) {
    var dataEl = container.querySelector("script.larnix-quiz-data");
    if (!dataEl) return;

    var quiz;
    try {
      quiz = JSON.parse(dataEl.textContent);
    } catch (e) {
      container.appendChild(el("p", "larnix-quiz-error", "Could not load this quiz."));
      return;
    }

    var questions = quiz.questions || [];
    var quizId = quiz.id || quiz.title || (location.pathname + "#quiz");

    container.innerHTML = "";
    if (quiz.title) container.appendChild(el("h3", "larnix-quiz-title", quiz.title));

    var form = el("form", "larnix-quiz-form");
    var items = [];

    questions.forEach(function (q, qi) {
      var fs = el("fieldset", "larnix-quiz-q");
      fs.appendChild(el("legend", "larnix-quiz-prompt", qi + 1 + ". " + (q.prompt || "")));
      var name = "q" + qi;
      (q.options || []).forEach(function (opt, oi) {
        var lab = el("label", "larnix-quiz-option");
        var inp = el("input");
        inp.type = "radio";
        inp.name = name;
        inp.value = String(oi);
        lab.appendChild(inp);
        lab.appendChild(el("span", "larnix-quiz-option-text", " " + opt));
        fs.appendChild(lab);
      });
      var fb = el("div", "larnix-quiz-feedback");
      fb.hidden = true;
      fs.appendChild(fb);
      form.appendChild(fs);
      items.push({ fieldset: fs, feedback: fb, q: q });
    });

    var submit = el("button", "larnix-quiz-submit", "Check answers");
    submit.type = "submit";
    form.appendChild(submit);

    var score = el("div", "larnix-quiz-score");
    score.setAttribute("role", "status");
    score.hidden = true;
    form.appendChild(score);

    form.addEventListener("submit", function (ev) {
      ev.preventDefault();
      var correct = 0;
      items.forEach(function (item, qi) {
        var sel = form.querySelector('input[name="q' + qi + '"]:checked');
        var ans = parseInt(item.q.answer, 10);
        var expl = item.q.explanation || "";
        item.feedback.hidden = false;
        item.fieldset.classList.remove("is-correct", "is-incorrect");
        if (sel && parseInt(sel.value, 10) === ans) {
          correct++;
          item.fieldset.classList.add("is-correct");
          item.feedback.textContent = "✅ Correct. " + expl;
        } else {
          item.fieldset.classList.add("is-incorrect");
          var lead = sel ? "❌ Not quite. " : "❌ No answer selected. ";
          item.feedback.textContent = lead + expl;
        }
      });

      var total = items.length;
      var prev = loadProgress(quizId);
      var best = prev && typeof prev.best === "number" ? Math.max(prev.best, correct) : correct;
      saveProgress(quizId, {
        best: best,
        last: correct,
        total: total,
        at: new Date().toISOString(),
      });

      score.hidden = false;
      score.textContent = "You scored " + correct + " / " + total + ".";
      if (best > correct) score.textContent += " Best: " + best + " / " + total + ".";
    });

    container.appendChild(form);

    var prior = loadProgress(quizId);
    if (prior && typeof prior.best === "number") {
      container.appendChild(
        el(
          "p",
          "larnix-quiz-prior",
          "Your best so far: " + prior.best + " / " + (prior.total || questions.length) + "."
        )
      );
    }
  }

  function init() {
    var nodes = document.querySelectorAll(".larnix-quiz[data-larnix-quiz]");
    Array.prototype.forEach.call(nodes, renderQuiz);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
