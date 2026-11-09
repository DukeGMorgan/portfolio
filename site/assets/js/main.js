/* ============================================================
   Duke Morgan — portfolio behaviour
   No dependencies. Degrades cleanly if JS is unavailable.
   ============================================================ */
(function () {
  'use strict';

  var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------- footer year ---------- */
  var yearEl = document.getElementById('year');
  if (yearEl) yearEl.textContent = String(new Date().getFullYear());

  /* ---------- scroll progress + sticky nav ---------- */
  var bar = document.querySelector('.scroll-progress span');
  var nav = document.getElementById('nav');
  var ticking = false;

  function onScroll() {
    var y = window.scrollY || document.documentElement.scrollTop;
    var max = document.documentElement.scrollHeight - window.innerHeight;

    if (bar) {
      var pct = max > 0 ? Math.min(y / max, 1) : 0;
      bar.style.transform = 'scaleX(' + pct + ')';
    }
    if (nav) nav.classList.toggle('is-stuck', y > 12);

    ticking = false;
  }

  window.addEventListener('scroll', function () {
    if (!ticking) {
      window.requestAnimationFrame(onScroll);
      ticking = true;
    }
  }, { passive: true });
  onScroll();

  /* ---------- mobile nav ---------- */
  var toggle = document.querySelector('.nav__toggle');
  var links = document.querySelector('.nav__links');

  if (toggle && links) {
    toggle.addEventListener('click', function () {
      var open = toggle.getAttribute('aria-expanded') === 'true';
      toggle.setAttribute('aria-expanded', String(!open));
      links.classList.toggle('is-open', !open);
    });

    links.addEventListener('click', function (e) {
      if (e.target.tagName === 'A') {
        toggle.setAttribute('aria-expanded', 'false');
        links.classList.remove('is-open');
      }
    });
  }

  /* ---------- reveal on scroll ---------- */
  var revealables = document.querySelectorAll('.reveal');

  if (reduceMotion || !('IntersectionObserver' in window)) {
    Array.prototype.forEach.call(revealables, function (el) {
      el.classList.add('is-in');
    });
  } else {
    var revealObserver = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-in');
          revealObserver.unobserve(entry.target);
        }
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -8% 0px' });

    Array.prototype.forEach.call(revealables, function (el) {
      revealObserver.observe(el);
    });
  }

  /* ---------- animated stat counters ---------- */
  var stats = document.querySelectorAll('.stat__num[data-count]');

  function formatNumber(n) {
    return n.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');
  }

  function runCounter(el) {
    var target = parseFloat(el.getAttribute('data-count'));
    var prefix = el.getAttribute('data-prefix') || '';
    var suffix = el.getAttribute('data-suffix') || '';
    var duration = 1400;
    var start = null;

    function step(ts) {
      if (start === null) start = ts;
      var p = Math.min((ts - start) / duration, 1);
      // ease-out cubic
      var eased = 1 - Math.pow(1 - p, 3);
      var value = Math.round(target * eased);
      el.textContent = prefix + formatNumber(value) + suffix;
      if (p < 1) window.requestAnimationFrame(step);
    }

    window.requestAnimationFrame(step);
  }

  if (!reduceMotion && 'IntersectionObserver' in window && stats.length) {
    var statObserver = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          runCounter(entry.target);
          statObserver.unobserve(entry.target);
        }
      });
    }, { threshold: 0.55 });

    Array.prototype.forEach.call(stats, function (el) {
      statObserver.observe(el);
    });
  }

  /* ---------- active section in nav ---------- */
  var sections = document.querySelectorAll('main section[id]');
  var navLinks = document.querySelectorAll('.nav__links a[href^="#"]');

  if ('IntersectionObserver' in window && sections.length) {
    var sectionObserver = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        var id = entry.target.getAttribute('id');
        Array.prototype.forEach.call(navLinks, function (a) {
          a.classList.toggle('is-active', a.getAttribute('href') === '#' + id);
        });
      });
    }, { rootMargin: '-45% 0px -50% 0px' });

    Array.prototype.forEach.call(sections, function (s) {
      sectionObserver.observe(s);
    });
  }

  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && toggle && links && links.classList.contains('is-open')) {
      toggle.setAttribute('aria-expanded', 'false');
      links.classList.remove('is-open');
      toggle.focus();
    }
  });

  /* ---------- Interactive Multi-Agent RAG Architecture Blueprint ---------- */
  var ragPlanes = document.querySelectorAll('.rag-plane[data-plane]');
  var ragRunBtn = document.getElementById('rag-run-btn');
  var ragResetBtn = document.getElementById('rag-reset-btn');
  var ragBanner = document.getElementById('rag-sim-banner');
  var ragStepLabel = document.getElementById('rag-step-label');
  var ragStatusPill = document.getElementById('rag-status-pill');
  var ragBtnText = document.getElementById('rag-btn-text');

  var ragPlaneData = {
    1: {
      tag: 'PLANE 01 DEEP-DIVE',
      title: 'Contextual Ingestion & Enrichment Plane',
      slo: 'Throughput: 450 pgs/min',
      desc: 'Ingests raw enterprise and clinical documents (PDFs, protocol notes, regulatory filings, transcripts). Extracts hierarchical layout structure, preserves table headers, and injects parent-child lineage alongside role-based ACL metadata before indexing.',
      stack: ['Layout-Aware Parsing', 'Unstructured Pipeline', 'Dynamic Chunking (256-512)', 'Redis Task Queue', 'Parquet Lineage Store'],
      telemetry: [
        { label: 'Layout Parse F1:', val: '99.4%' },
        { label: 'ACL Metadata Tags:', val: '12 attributes' },
        { label: 'Index Sync Latency:', val: '< 1.2s', hi: true }
      ]
    },
    2: {
      tag: 'PLANE 02 DEEP-DIVE',
      title: 'Hybrid Two-Tier Retrieval Plane',
      slo: 'Combined Latency: 42ms',
      desc: 'Executes parallel retrieval: dense semantic vectors (HNSW index) capture clinical and conceptual context, while sparse BM25 lexical search captures exact alphanumeric codes, medications, and identifiers. Candidates merge via Reciprocal Rank Fusion (RRF) and a cross-encoder reranker.',
      stack: ['Dense Vector HNSW', 'BM25 Sparse Lexical', 'Reciprocal Rank Fusion', 'Cross-Encoder Reranker', 'FastAPI Gateway'],
      telemetry: [
        { label: 'Vector Search (p95):', val: '14ms' },
        { label: 'Reranker Scoring (p99):', val: '28ms' },
        { label: 'Recall @ Top-5:', val: '96.8%', hi: true }
      ]
    },
    3: {
      tag: 'PLANE 03 DEEP-DIVE',
      title: 'Agentic State Graph & Orchestrator',
      slo: 'Concurrency: 60 tasks/s',
      desc: 'Built on a stateful cyclic graph router. A supervisor evaluates query intent: straightforward lookups route directly, while multi-part clinical or operational questions decompose into parallel sub-tasks dispatched to domain-scoped specialist agents.',
      stack: ['Stateful Agent Graph', 'Supervisor Router', 'Domain Sub-Agents', 'Azure AI Foundry / Claude / OpenAI', 'Structured Outputs'],
      telemetry: [
        { label: 'Routing Overhead:', val: '85ms' },
        { label: 'Parallel Specialists:', val: '3 Workers avg' },
        { label: 'Task Convergence:', val: '99.1%', hi: true }
      ]
    },
    4: {
      tag: 'PLANE 04 DEEP-DIVE',
      title: 'Governance & Deterministic Guardrails',
      slo: 'Attribution Floor: 0.85',
      desc: 'Enforces clinical-grade trust with inline validation gates. Pre-inference filters scrub PII/PHI and enforce data-lane policy; post-synthesis evaluators verify entailment against retrieved source chunks before any response reaches the user.',
      stack: ['Inline Guardrail Gate', 'Ragas Faithfulness Eval', 'PII / PHI Redaction', 'OpenTelemetry Audit', 'Deterministic Fallback'],
      telemetry: [
        { label: 'Faithfulness Score:', val: '0.94 avg', hi: true },
        { label: 'Unauthorized Egress:', val: '0.000%' },
        { label: 'Audit Trace Overhead:', val: '< 6ms' }
      ]
    }
  };

  function selectRagPlane(planeId) {
    var data = ragPlaneData[planeId];
    if (!data) return;

    Array.prototype.forEach.call(ragPlanes, function (btn) {
      var active = String(btn.getAttribute('data-plane')) === String(planeId);
      btn.classList.toggle('is-active', active);
      btn.setAttribute('aria-selected', String(active));
    });

    var tagEl = document.getElementById('rag-detail-tag');
    var titleEl = document.getElementById('rag-detail-title');
    var sloEl = document.getElementById('rag-detail-slo');
    var descEl = document.getElementById('rag-detail-desc');
    var stackEl = document.getElementById('rag-detail-stack');
    var telEl = document.getElementById('rag-detail-telemetry');

    if (tagEl) tagEl.textContent = data.tag;
    if (titleEl) titleEl.textContent = data.title;
    if (sloEl) sloEl.textContent = data.slo;
    if (descEl) descEl.textContent = data.desc;

    if (stackEl) {
      stackEl.innerHTML = data.stack.map(function (s) {
        return '<span>' + s + '</span>';
      }).join('');
    }
    if (telEl) {
      telEl.innerHTML = data.telemetry.map(function (t) {
        var cls = t.hi ? 'rag-telemetry__val rag-telemetry__val--hi' : 'rag-telemetry__val';
        return '<div class="rag-telemetry__row"><span class="rag-telemetry__label">' + t.label +
               '</span><span class="' + cls + '">' + t.val + '</span></div>';
      }).join('');
    }
  }

  if (ragPlanes.length) {
    Array.prototype.forEach.call(ragPlanes, function (btn) {
      btn.addEventListener('click', function () {
        selectRagPlane(btn.getAttribute('data-plane'));
      });
    });

    var simSteps = [
      { plane: 1, label: 'Plane 01: Layout Parse & ACL Check', status: 'Validating schema & RBAC tags...', node: 'rag-node-1-1' },
      { plane: 2, label: 'Plane 02: Hybrid Search (Dense + BM25)', status: 'Fusing candidates via Reciprocal Rank Fusion...', node: 'rag-node-2-1' },
      { plane: 2, label: 'Plane 02: Cross-Encoder Reranking', status: 'Pruning context window to top-5 chunks (<28ms)...', node: 'rag-node-2-3' },
      { plane: 3, label: 'Plane 03: Supervisor Dispatches Agents', status: 'Routing sub-queries across specialist workers...', node: 'rag-node-3-1' },
      { plane: 3, label: 'Plane 03: Multi-Agent Context Synthesis', status: 'Reconciling multi-facility protocol records...', node: 'rag-node-3-3' },
      { plane: 4, label: 'Plane 04: Deterministic Faithfulness Gate', status: 'Source attribution verified (0.94 entailment)...', node: 'rag-node-4-1' },
      { plane: 4, label: 'Complete: Governed Output Delivered', status: 'OpenTelemetry audit lineage committed (214ms).', node: 'rag-node-4-3' }
    ];

    var simTimer = null;
    var simIdx = 0;
    var isSimRunning = false;

    function clearNodeFlashes() {
      var nodes = document.querySelectorAll('.rag-node.is-flashing');
      Array.prototype.forEach.call(nodes, function (n) {
        n.classList.remove('is-flashing');
      });
    }

    function stepSimulation() {
      if (simIdx >= simSteps.length) {
        window.clearInterval(simTimer);
        simTimer = null;
        isSimRunning = false;
        if (ragStepLabel) ragStepLabel.textContent = 'Complete (214ms)';
        if (ragStatusPill) ragStatusPill.textContent = 'Status: Verified & Audited (SLO Met)';
        if (ragBtnText) ragBtnText.textContent = 'Replay Query Trace';
        return;
      }

      var cur = simSteps[simIdx];
      selectRagPlane(cur.plane);
      if (ragStepLabel) ragStepLabel.textContent = cur.label;
      if (ragStatusPill) ragStatusPill.textContent = cur.status;

      clearNodeFlashes();
      var nodeEl = document.getElementById(cur.node);
      if (nodeEl) {
        nodeEl.classList.add('is-flashing');
      }
      simIdx += 1;
    }

    function resetSimulation() {
      if (simTimer) {
        window.clearInterval(simTimer);
        simTimer = null;
      }
      isSimRunning = false;
      simIdx = 0;
      clearNodeFlashes();
      if (ragBanner) ragBanner.classList.remove('is-visible');
      if (ragStepLabel) ragStepLabel.textContent = 'Idle / Ready';
      if (ragBtnText) ragBtnText.textContent = 'Trace Sample Request';
      selectRagPlane(1);
    }

    if (ragRunBtn) {
      ragRunBtn.addEventListener('click', function () {
        if (isSimRunning) {
          resetSimulation();
          return;
        }
        isSimRunning = true;
        simIdx = 0;
        if (ragBanner) ragBanner.classList.add('is-visible');
        if (ragBtnText) ragBtnText.textContent = 'Stop Trace';
        stepSimulation();
        simTimer = window.setInterval(stepSimulation, 1650);
      });
    }

    if (ragResetBtn) {
      ragResetBtn.addEventListener('click', resetSimulation);
    }
  }

  /* ---------- Progressive Disclosure: Architecture Deck & Case Tabs ---------- */
  var archTabs = document.querySelectorAll('.arch-tab[data-arch-tab]');
  var archPanels = document.querySelectorAll('.arch-panel[data-arch-panel]');

  Array.prototype.forEach.call(archTabs, function (tab) {
    tab.addEventListener('click', function () {
      var target = tab.getAttribute('data-arch-tab');
      Array.prototype.forEach.call(archTabs, function (t) {
        var active = t.getAttribute('data-arch-tab') === target;
        t.classList.toggle('is-active', active);
        t.setAttribute('aria-selected', String(active));
      });
      Array.prototype.forEach.call(archPanels, function (p) {
        p.classList.toggle('is-active', p.getAttribute('data-arch-panel') === target);
      });
    });
  });

  var caseTabs = document.querySelectorAll('.case-tab[data-case-tab]');
  var casePanels = document.querySelectorAll('.case-panel[data-case-panel]');

  Array.prototype.forEach.call(caseTabs, function (tab) {
    tab.addEventListener('click', function () {
      var target = tab.getAttribute('data-case-tab');
      Array.prototype.forEach.call(caseTabs, function (t) {
        var active = t.getAttribute('data-case-tab') === target;
        t.classList.toggle('is-active', active);
        t.setAttribute('aria-selected', String(active));
      });
      Array.prototype.forEach.call(casePanels, function (p) {
        p.classList.toggle('is-active', p.getAttribute('data-case-panel') === target);
      });
    });
  });

  /* ---------- One-click Copy Email convenience ---------- */
  var emailLink = document.getElementById('email-link');
  var emailText = document.getElementById('email-text');
  if (emailLink && emailText && navigator.clipboard) {
    emailLink.addEventListener('click', function () {
      navigator.clipboard.writeText('Dukeisrn@me.com').then(function () {
        var orig = emailText.textContent;
        emailText.textContent = 'Copied: Dukeisrn@me.com';
        window.setTimeout(function () {
          emailText.textContent = orig;
        }, 2800);
      }).catch(function () {});
    });
  }
})();
