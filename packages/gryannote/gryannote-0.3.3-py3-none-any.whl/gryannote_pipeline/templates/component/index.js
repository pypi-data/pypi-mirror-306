const {
  SvelteComponent: wn,
  assign: pn,
  create_slot: kn,
  detach: vn,
  element: yn,
  get_all_dirty_from_scope: Cn,
  get_slot_changes: jn,
  get_spread_update: qn,
  init: Sn,
  insert: En,
  safe_not_equal: Nn,
  set_dynamic_element_data: Jl,
  set_style: W,
  toggle_class: Ce,
  transition_in: Jt,
  transition_out: Rt,
  update_slot_base: Fn
} = window.__gradio__svelte__internal;
function Ln(t) {
  let l, e, n;
  const i = (
    /*#slots*/
    t[18].default
  ), f = kn(
    i,
    t,
    /*$$scope*/
    t[17],
    null
  );
  let u = [
    { "data-testid": (
      /*test_id*/
      t[7]
    ) },
    { id: (
      /*elem_id*/
      t[2]
    ) },
    {
      class: e = "block " + /*elem_classes*/
      t[3].join(" ") + " svelte-1t38q2d"
    }
  ], o = {};
  for (let s = 0; s < u.length; s += 1)
    o = pn(o, u[s]);
  return {
    c() {
      l = yn(
        /*tag*/
        t[14]
      ), f && f.c(), Jl(
        /*tag*/
        t[14]
      )(l, o), Ce(
        l,
        "hidden",
        /*visible*/
        t[10] === !1
      ), Ce(
        l,
        "padded",
        /*padding*/
        t[6]
      ), Ce(
        l,
        "border_focus",
        /*border_mode*/
        t[5] === "focus"
      ), Ce(l, "hide-container", !/*explicit_call*/
      t[8] && !/*container*/
      t[9]), W(
        l,
        "height",
        /*get_dimension*/
        t[15](
          /*height*/
          t[0]
        )
      ), W(l, "width", typeof /*width*/
      t[1] == "number" ? `calc(min(${/*width*/
      t[1]}px, 100%))` : (
        /*get_dimension*/
        t[15](
          /*width*/
          t[1]
        )
      )), W(
        l,
        "border-style",
        /*variant*/
        t[4]
      ), W(
        l,
        "overflow",
        /*allow_overflow*/
        t[11] ? "visible" : "hidden"
      ), W(
        l,
        "flex-grow",
        /*scale*/
        t[12]
      ), W(l, "min-width", `calc(min(${/*min_width*/
      t[13]}px, 100%))`), W(l, "border-width", "var(--block-border-width)");
    },
    m(s, r) {
      En(s, l, r), f && f.m(l, null), n = !0;
    },
    p(s, r) {
      f && f.p && (!n || r & /*$$scope*/
      131072) && Fn(
        f,
        i,
        s,
        /*$$scope*/
        s[17],
        n ? jn(
          i,
          /*$$scope*/
          s[17],
          r,
          null
        ) : Cn(
          /*$$scope*/
          s[17]
        ),
        null
      ), Jl(
        /*tag*/
        s[14]
      )(l, o = qn(u, [
        (!n || r & /*test_id*/
        128) && { "data-testid": (
          /*test_id*/
          s[7]
        ) },
        (!n || r & /*elem_id*/
        4) && { id: (
          /*elem_id*/
          s[2]
        ) },
        (!n || r & /*elem_classes*/
        8 && e !== (e = "block " + /*elem_classes*/
        s[3].join(" ") + " svelte-1t38q2d")) && { class: e }
      ])), Ce(
        l,
        "hidden",
        /*visible*/
        s[10] === !1
      ), Ce(
        l,
        "padded",
        /*padding*/
        s[6]
      ), Ce(
        l,
        "border_focus",
        /*border_mode*/
        s[5] === "focus"
      ), Ce(l, "hide-container", !/*explicit_call*/
      s[8] && !/*container*/
      s[9]), r & /*height*/
      1 && W(
        l,
        "height",
        /*get_dimension*/
        s[15](
          /*height*/
          s[0]
        )
      ), r & /*width*/
      2 && W(l, "width", typeof /*width*/
      s[1] == "number" ? `calc(min(${/*width*/
      s[1]}px, 100%))` : (
        /*get_dimension*/
        s[15](
          /*width*/
          s[1]
        )
      )), r & /*variant*/
      16 && W(
        l,
        "border-style",
        /*variant*/
        s[4]
      ), r & /*allow_overflow*/
      2048 && W(
        l,
        "overflow",
        /*allow_overflow*/
        s[11] ? "visible" : "hidden"
      ), r & /*scale*/
      4096 && W(
        l,
        "flex-grow",
        /*scale*/
        s[12]
      ), r & /*min_width*/
      8192 && W(l, "min-width", `calc(min(${/*min_width*/
      s[13]}px, 100%))`);
    },
    i(s) {
      n || (Jt(f, s), n = !0);
    },
    o(s) {
      Rt(f, s), n = !1;
    },
    d(s) {
      s && vn(l), f && f.d(s);
    }
  };
}
function Mn(t) {
  let l, e = (
    /*tag*/
    t[14] && Ln(t)
  );
  return {
    c() {
      e && e.c();
    },
    m(n, i) {
      e && e.m(n, i), l = !0;
    },
    p(n, [i]) {
      /*tag*/
      n[14] && e.p(n, i);
    },
    i(n) {
      l || (Jt(e, n), l = !0);
    },
    o(n) {
      Rt(e, n), l = !1;
    },
    d(n) {
      e && e.d(n);
    }
  };
}
function zn(t, l, e) {
  let { $$slots: n = {}, $$scope: i } = l, { height: f = void 0 } = l, { width: u = void 0 } = l, { elem_id: o = "" } = l, { elem_classes: s = [] } = l, { variant: r = "solid" } = l, { border_mode: a = "base" } = l, { padding: m = !0 } = l, { type: p = "normal" } = l, { test_id: g = void 0 } = l, { explicit_call: j = !1 } = l, { container: k = !0 } = l, { visible: d = !0 } = l, { allow_overflow: _ = !0 } = l, { scale: w = null } = l, { min_width: c = 0 } = l, h = p === "fieldset" ? "fieldset" : "div";
  const q = (v) => {
    if (v !== void 0) {
      if (typeof v == "number")
        return v + "px";
      if (typeof v == "string")
        return v;
    }
  };
  return t.$$set = (v) => {
    "height" in v && e(0, f = v.height), "width" in v && e(1, u = v.width), "elem_id" in v && e(2, o = v.elem_id), "elem_classes" in v && e(3, s = v.elem_classes), "variant" in v && e(4, r = v.variant), "border_mode" in v && e(5, a = v.border_mode), "padding" in v && e(6, m = v.padding), "type" in v && e(16, p = v.type), "test_id" in v && e(7, g = v.test_id), "explicit_call" in v && e(8, j = v.explicit_call), "container" in v && e(9, k = v.container), "visible" in v && e(10, d = v.visible), "allow_overflow" in v && e(11, _ = v.allow_overflow), "scale" in v && e(12, w = v.scale), "min_width" in v && e(13, c = v.min_width), "$$scope" in v && e(17, i = v.$$scope);
  }, [
    f,
    u,
    o,
    s,
    r,
    a,
    m,
    g,
    j,
    k,
    d,
    _,
    w,
    c,
    h,
    q,
    p,
    i,
    n
  ];
}
class On extends wn {
  constructor(l) {
    super(), Sn(this, l, zn, Mn, Nn, {
      height: 0,
      width: 1,
      elem_id: 2,
      elem_classes: 3,
      variant: 4,
      border_mode: 5,
      padding: 6,
      type: 16,
      test_id: 7,
      explicit_call: 8,
      container: 9,
      visible: 10,
      allow_overflow: 11,
      scale: 12,
      min_width: 13
    });
  }
}
const {
  SvelteComponent: An,
  attr: Vn,
  create_slot: Dn,
  detach: Bn,
  element: Tn,
  get_all_dirty_from_scope: Un,
  get_slot_changes: Zn,
  init: Pn,
  insert: In,
  safe_not_equal: Hn,
  transition_in: Jn,
  transition_out: Rn,
  update_slot_base: Xn
} = window.__gradio__svelte__internal;
function Yn(t) {
  let l, e;
  const n = (
    /*#slots*/
    t[1].default
  ), i = Dn(
    n,
    t,
    /*$$scope*/
    t[0],
    null
  );
  return {
    c() {
      l = Tn("div"), i && i.c(), Vn(l, "class", "svelte-1hnfib2");
    },
    m(f, u) {
      In(f, l, u), i && i.m(l, null), e = !0;
    },
    p(f, [u]) {
      i && i.p && (!e || u & /*$$scope*/
      1) && Xn(
        i,
        n,
        f,
        /*$$scope*/
        f[0],
        e ? Zn(
          n,
          /*$$scope*/
          f[0],
          u,
          null
        ) : Un(
          /*$$scope*/
          f[0]
        ),
        null
      );
    },
    i(f) {
      e || (Jn(i, f), e = !0);
    },
    o(f) {
      Rn(i, f), e = !1;
    },
    d(f) {
      f && Bn(l), i && i.d(f);
    }
  };
}
function Gn(t, l, e) {
  let { $$slots: n = {}, $$scope: i } = l;
  return t.$$set = (f) => {
    "$$scope" in f && e(0, i = f.$$scope);
  }, [i, n];
}
class Kn extends An {
  constructor(l) {
    super(), Pn(this, l, Gn, Yn, Hn, {});
  }
}
const {
  SvelteComponent: Qn,
  attr: Rl,
  check_outros: Wn,
  create_component: xn,
  create_slot: $n,
  destroy_component: ei,
  detach: sl,
  element: li,
  empty: ti,
  get_all_dirty_from_scope: ni,
  get_slot_changes: ii,
  group_outros: si,
  init: oi,
  insert: ol,
  mount_component: fi,
  safe_not_equal: ui,
  set_data: ri,
  space: ai,
  text: _i,
  toggle_class: Le,
  transition_in: Ye,
  transition_out: fl,
  update_slot_base: ci
} = window.__gradio__svelte__internal;
function Xl(t) {
  let l, e;
  return l = new Kn({
    props: {
      $$slots: { default: [di] },
      $$scope: { ctx: t }
    }
  }), {
    c() {
      xn(l.$$.fragment);
    },
    m(n, i) {
      fi(l, n, i), e = !0;
    },
    p(n, i) {
      const f = {};
      i & /*$$scope, info*/
      10 && (f.$$scope = { dirty: i, ctx: n }), l.$set(f);
    },
    i(n) {
      e || (Ye(l.$$.fragment, n), e = !0);
    },
    o(n) {
      fl(l.$$.fragment, n), e = !1;
    },
    d(n) {
      ei(l, n);
    }
  };
}
function di(t) {
  let l;
  return {
    c() {
      l = _i(
        /*info*/
        t[1]
      );
    },
    m(e, n) {
      ol(e, l, n);
    },
    p(e, n) {
      n & /*info*/
      2 && ri(
        l,
        /*info*/
        e[1]
      );
    },
    d(e) {
      e && sl(l);
    }
  };
}
function mi(t) {
  let l, e, n, i;
  const f = (
    /*#slots*/
    t[2].default
  ), u = $n(
    f,
    t,
    /*$$scope*/
    t[3],
    null
  );
  let o = (
    /*info*/
    t[1] && Xl(t)
  );
  return {
    c() {
      l = li("span"), u && u.c(), e = ai(), o && o.c(), n = ti(), Rl(l, "data-testid", "block-info"), Rl(l, "class", "svelte-22c38v"), Le(l, "sr-only", !/*show_label*/
      t[0]), Le(l, "hide", !/*show_label*/
      t[0]), Le(
        l,
        "has-info",
        /*info*/
        t[1] != null
      );
    },
    m(s, r) {
      ol(s, l, r), u && u.m(l, null), ol(s, e, r), o && o.m(s, r), ol(s, n, r), i = !0;
    },
    p(s, [r]) {
      u && u.p && (!i || r & /*$$scope*/
      8) && ci(
        u,
        f,
        s,
        /*$$scope*/
        s[3],
        i ? ii(
          f,
          /*$$scope*/
          s[3],
          r,
          null
        ) : ni(
          /*$$scope*/
          s[3]
        ),
        null
      ), (!i || r & /*show_label*/
      1) && Le(l, "sr-only", !/*show_label*/
      s[0]), (!i || r & /*show_label*/
      1) && Le(l, "hide", !/*show_label*/
      s[0]), (!i || r & /*info*/
      2) && Le(
        l,
        "has-info",
        /*info*/
        s[1] != null
      ), /*info*/
      s[1] ? o ? (o.p(s, r), r & /*info*/
      2 && Ye(o, 1)) : (o = Xl(s), o.c(), Ye(o, 1), o.m(n.parentNode, n)) : o && (si(), fl(o, 1, 1, () => {
        o = null;
      }), Wn());
    },
    i(s) {
      i || (Ye(u, s), Ye(o), i = !0);
    },
    o(s) {
      fl(u, s), fl(o), i = !1;
    },
    d(s) {
      s && (sl(l), sl(e), sl(n)), u && u.d(s), o && o.d(s);
    }
  };
}
function bi(t, l, e) {
  let { $$slots: n = {}, $$scope: i } = l, { show_label: f = !0 } = l, { info: u = void 0 } = l;
  return t.$$set = (o) => {
    "show_label" in o && e(0, f = o.show_label), "info" in o && e(1, u = o.info), "$$scope" in o && e(3, i = o.$$scope);
  }, [f, u, n, i];
}
class Xt extends Qn {
  constructor(l) {
    super(), oi(this, l, bi, mi, ui, { show_label: 0, info: 1 });
  }
}
const {
  SvelteComponent: hi,
  append: gi,
  attr: Me,
  detach: wi,
  init: pi,
  insert: ki,
  noop: yl,
  safe_not_equal: vi,
  svg_element: Yl
} = window.__gradio__svelte__internal;
function yi(t) {
  let l, e;
  return {
    c() {
      l = Yl("svg"), e = Yl("path"), Me(e, "d", "M5 8l4 4 4-4z"), Me(l, "class", "dropdown-arrow svelte-145leq6"), Me(l, "xmlns", "http://www.w3.org/2000/svg"), Me(l, "width", "100%"), Me(l, "height", "100%"), Me(l, "viewBox", "0 0 18 18");
    },
    m(n, i) {
      ki(n, l, i), gi(l, e);
    },
    p: yl,
    i: yl,
    o: yl,
    d(n) {
      n && wi(l);
    }
  };
}
class Yt extends hi {
  constructor(l) {
    super(), pi(this, l, null, yi, vi, {});
  }
}
const {
  SvelteComponent: Ci,
  append: ji,
  attr: Cl,
  detach: qi,
  init: Si,
  insert: Ei,
  noop: jl,
  safe_not_equal: Ni,
  svg_element: Gl
} = window.__gradio__svelte__internal;
function Fi(t) {
  let l, e;
  return {
    c() {
      l = Gl("svg"), e = Gl("path"), Cl(e, "d", "M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"), Cl(l, "xmlns", "http://www.w3.org/2000/svg"), Cl(l, "viewBox", "0 0 24 24");
    },
    m(n, i) {
      Ei(n, l, i), ji(l, e);
    },
    p: jl,
    i: jl,
    o: jl,
    d(n) {
      n && qi(l);
    }
  };
}
class Gt extends Ci {
  constructor(l) {
    super(), Si(this, l, null, Fi, Ni, {});
  }
}
const Li = [
  { color: "red", primary: 600, secondary: 100 },
  { color: "green", primary: 600, secondary: 100 },
  { color: "blue", primary: 600, secondary: 100 },
  { color: "yellow", primary: 500, secondary: 100 },
  { color: "purple", primary: 600, secondary: 100 },
  { color: "teal", primary: 600, secondary: 100 },
  { color: "orange", primary: 600, secondary: 100 },
  { color: "cyan", primary: 600, secondary: 100 },
  { color: "lime", primary: 500, secondary: 100 },
  { color: "pink", primary: 600, secondary: 100 }
], Kl = {
  inherit: "inherit",
  current: "currentColor",
  transparent: "transparent",
  black: "#000",
  white: "#fff",
  slate: {
    50: "#f8fafc",
    100: "#f1f5f9",
    200: "#e2e8f0",
    300: "#cbd5e1",
    400: "#94a3b8",
    500: "#64748b",
    600: "#475569",
    700: "#334155",
    800: "#1e293b",
    900: "#0f172a",
    950: "#020617"
  },
  gray: {
    50: "#f9fafb",
    100: "#f3f4f6",
    200: "#e5e7eb",
    300: "#d1d5db",
    400: "#9ca3af",
    500: "#6b7280",
    600: "#4b5563",
    700: "#374151",
    800: "#1f2937",
    900: "#111827",
    950: "#030712"
  },
  zinc: {
    50: "#fafafa",
    100: "#f4f4f5",
    200: "#e4e4e7",
    300: "#d4d4d8",
    400: "#a1a1aa",
    500: "#71717a",
    600: "#52525b",
    700: "#3f3f46",
    800: "#27272a",
    900: "#18181b",
    950: "#09090b"
  },
  neutral: {
    50: "#fafafa",
    100: "#f5f5f5",
    200: "#e5e5e5",
    300: "#d4d4d4",
    400: "#a3a3a3",
    500: "#737373",
    600: "#525252",
    700: "#404040",
    800: "#262626",
    900: "#171717",
    950: "#0a0a0a"
  },
  stone: {
    50: "#fafaf9",
    100: "#f5f5f4",
    200: "#e7e5e4",
    300: "#d6d3d1",
    400: "#a8a29e",
    500: "#78716c",
    600: "#57534e",
    700: "#44403c",
    800: "#292524",
    900: "#1c1917",
    950: "#0c0a09"
  },
  red: {
    50: "#fef2f2",
    100: "#fee2e2",
    200: "#fecaca",
    300: "#fca5a5",
    400: "#f87171",
    500: "#ef4444",
    600: "#dc2626",
    700: "#b91c1c",
    800: "#991b1b",
    900: "#7f1d1d",
    950: "#450a0a"
  },
  orange: {
    50: "#fff7ed",
    100: "#ffedd5",
    200: "#fed7aa",
    300: "#fdba74",
    400: "#fb923c",
    500: "#f97316",
    600: "#ea580c",
    700: "#c2410c",
    800: "#9a3412",
    900: "#7c2d12",
    950: "#431407"
  },
  amber: {
    50: "#fffbeb",
    100: "#fef3c7",
    200: "#fde68a",
    300: "#fcd34d",
    400: "#fbbf24",
    500: "#f59e0b",
    600: "#d97706",
    700: "#b45309",
    800: "#92400e",
    900: "#78350f",
    950: "#451a03"
  },
  yellow: {
    50: "#fefce8",
    100: "#fef9c3",
    200: "#fef08a",
    300: "#fde047",
    400: "#facc15",
    500: "#eab308",
    600: "#ca8a04",
    700: "#a16207",
    800: "#854d0e",
    900: "#713f12",
    950: "#422006"
  },
  lime: {
    50: "#f7fee7",
    100: "#ecfccb",
    200: "#d9f99d",
    300: "#bef264",
    400: "#a3e635",
    500: "#84cc16",
    600: "#65a30d",
    700: "#4d7c0f",
    800: "#3f6212",
    900: "#365314",
    950: "#1a2e05"
  },
  green: {
    50: "#f0fdf4",
    100: "#dcfce7",
    200: "#bbf7d0",
    300: "#86efac",
    400: "#4ade80",
    500: "#22c55e",
    600: "#16a34a",
    700: "#15803d",
    800: "#166534",
    900: "#14532d",
    950: "#052e16"
  },
  emerald: {
    50: "#ecfdf5",
    100: "#d1fae5",
    200: "#a7f3d0",
    300: "#6ee7b7",
    400: "#34d399",
    500: "#10b981",
    600: "#059669",
    700: "#047857",
    800: "#065f46",
    900: "#064e3b",
    950: "#022c22"
  },
  teal: {
    50: "#f0fdfa",
    100: "#ccfbf1",
    200: "#99f6e4",
    300: "#5eead4",
    400: "#2dd4bf",
    500: "#14b8a6",
    600: "#0d9488",
    700: "#0f766e",
    800: "#115e59",
    900: "#134e4a",
    950: "#042f2e"
  },
  cyan: {
    50: "#ecfeff",
    100: "#cffafe",
    200: "#a5f3fc",
    300: "#67e8f9",
    400: "#22d3ee",
    500: "#06b6d4",
    600: "#0891b2",
    700: "#0e7490",
    800: "#155e75",
    900: "#164e63",
    950: "#083344"
  },
  sky: {
    50: "#f0f9ff",
    100: "#e0f2fe",
    200: "#bae6fd",
    300: "#7dd3fc",
    400: "#38bdf8",
    500: "#0ea5e9",
    600: "#0284c7",
    700: "#0369a1",
    800: "#075985",
    900: "#0c4a6e",
    950: "#082f49"
  },
  blue: {
    50: "#eff6ff",
    100: "#dbeafe",
    200: "#bfdbfe",
    300: "#93c5fd",
    400: "#60a5fa",
    500: "#3b82f6",
    600: "#2563eb",
    700: "#1d4ed8",
    800: "#1e40af",
    900: "#1e3a8a",
    950: "#172554"
  },
  indigo: {
    50: "#eef2ff",
    100: "#e0e7ff",
    200: "#c7d2fe",
    300: "#a5b4fc",
    400: "#818cf8",
    500: "#6366f1",
    600: "#4f46e5",
    700: "#4338ca",
    800: "#3730a3",
    900: "#312e81",
    950: "#1e1b4b"
  },
  violet: {
    50: "#f5f3ff",
    100: "#ede9fe",
    200: "#ddd6fe",
    300: "#c4b5fd",
    400: "#a78bfa",
    500: "#8b5cf6",
    600: "#7c3aed",
    700: "#6d28d9",
    800: "#5b21b6",
    900: "#4c1d95",
    950: "#2e1065"
  },
  purple: {
    50: "#faf5ff",
    100: "#f3e8ff",
    200: "#e9d5ff",
    300: "#d8b4fe",
    400: "#c084fc",
    500: "#a855f7",
    600: "#9333ea",
    700: "#7e22ce",
    800: "#6b21a8",
    900: "#581c87",
    950: "#3b0764"
  },
  fuchsia: {
    50: "#fdf4ff",
    100: "#fae8ff",
    200: "#f5d0fe",
    300: "#f0abfc",
    400: "#e879f9",
    500: "#d946ef",
    600: "#c026d3",
    700: "#a21caf",
    800: "#86198f",
    900: "#701a75",
    950: "#4a044e"
  },
  pink: {
    50: "#fdf2f8",
    100: "#fce7f3",
    200: "#fbcfe8",
    300: "#f9a8d4",
    400: "#f472b6",
    500: "#ec4899",
    600: "#db2777",
    700: "#be185d",
    800: "#9d174d",
    900: "#831843",
    950: "#500724"
  },
  rose: {
    50: "#fff1f2",
    100: "#ffe4e6",
    200: "#fecdd3",
    300: "#fda4af",
    400: "#fb7185",
    500: "#f43f5e",
    600: "#e11d48",
    700: "#be123c",
    800: "#9f1239",
    900: "#881337",
    950: "#4c0519"
  }
};
Li.reduce(
  (t, { color: l, primary: e, secondary: n }) => ({
    ...t,
    [l]: {
      primary: Kl[l][e],
      secondary: Kl[l][n]
    }
  }),
  {}
);
function Ue(t) {
  let l = ["", "k", "M", "G", "T", "P", "E", "Z"], e = 0;
  for (; t > 1e3 && e < l.length - 1; )
    t /= 1e3, e++;
  let n = l[e];
  return (Number.isInteger(t) ? t : t.toFixed(1)) + n;
}
function ul() {
}
function Mi(t, l) {
  return t != t ? l == l : t !== l || t && typeof t == "object" || typeof t == "function";
}
function Ql(t) {
  const l = typeof t == "string" && t.match(/^\s*(-?[\d.]+)([^\s]*)\s*$/);
  return l ? [parseFloat(l[1]), l[2] || "px"] : [
    /** @type {number} */
    t,
    "px"
  ];
}
const Kt = typeof window < "u";
let Wl = Kt ? () => window.performance.now() : () => Date.now(), Qt = Kt ? (t) => requestAnimationFrame(t) : ul;
const Ie = /* @__PURE__ */ new Set();
function Wt(t) {
  Ie.forEach((l) => {
    l.c(t) || (Ie.delete(l), l.f());
  }), Ie.size !== 0 && Qt(Wt);
}
function zi(t) {
  let l;
  return Ie.size === 0 && Qt(Wt), {
    promise: new Promise((e) => {
      Ie.add(l = { c: t, f: e });
    }),
    abort() {
      Ie.delete(l);
    }
  };
}
function Oi(t) {
  const l = t - 1;
  return l * l * l + 1;
}
function xl(t, { delay: l = 0, duration: e = 400, easing: n = Oi, x: i = 0, y: f = 0, opacity: u = 0 } = {}) {
  const o = getComputedStyle(t), s = +o.opacity, r = o.transform === "none" ? "" : o.transform, a = s * (1 - u), [m, p] = Ql(i), [g, j] = Ql(f);
  return {
    delay: l,
    duration: e,
    easing: n,
    css: (k, d) => `
			transform: ${r} translate(${(1 - k) * m}${p}, ${(1 - k) * g}${j});
			opacity: ${s - a * d}`
  };
}
const ze = [];
function Ai(t, l = ul) {
  let e;
  const n = /* @__PURE__ */ new Set();
  function i(o) {
    if (Mi(t, o) && (t = o, e)) {
      const s = !ze.length;
      for (const r of n)
        r[1](), ze.push(r, t);
      if (s) {
        for (let r = 0; r < ze.length; r += 2)
          ze[r][0](ze[r + 1]);
        ze.length = 0;
      }
    }
  }
  function f(o) {
    i(o(t));
  }
  function u(o, s = ul) {
    const r = [o, s];
    return n.add(r), n.size === 1 && (e = l(i, f) || ul), o(t), () => {
      n.delete(r), n.size === 0 && e && (e(), e = null);
    };
  }
  return { set: i, update: f, subscribe: u };
}
function $l(t) {
  return Object.prototype.toString.call(t) === "[object Date]";
}
function Nl(t, l, e, n) {
  if (typeof e == "number" || $l(e)) {
    const i = n - e, f = (e - l) / (t.dt || 1 / 60), u = t.opts.stiffness * i, o = t.opts.damping * f, s = (u - o) * t.inv_mass, r = (f + s) * t.dt;
    return Math.abs(r) < t.opts.precision && Math.abs(i) < t.opts.precision ? n : (t.settled = !1, $l(e) ? new Date(e.getTime() + r) : e + r);
  } else {
    if (Array.isArray(e))
      return e.map(
        (i, f) => Nl(t, l[f], e[f], n[f])
      );
    if (typeof e == "object") {
      const i = {};
      for (const f in e)
        i[f] = Nl(t, l[f], e[f], n[f]);
      return i;
    } else
      throw new Error(`Cannot spring ${typeof e} values`);
  }
}
function et(t, l = {}) {
  const e = Ai(t), { stiffness: n = 0.15, damping: i = 0.8, precision: f = 0.01 } = l;
  let u, o, s, r = t, a = t, m = 1, p = 0, g = !1;
  function j(d, _ = {}) {
    a = d;
    const w = s = {};
    return t == null || _.hard || k.stiffness >= 1 && k.damping >= 1 ? (g = !0, u = Wl(), r = d, e.set(t = a), Promise.resolve()) : (_.soft && (p = 1 / ((_.soft === !0 ? 0.5 : +_.soft) * 60), m = 0), o || (u = Wl(), g = !1, o = zi((c) => {
      if (g)
        return g = !1, o = null, !1;
      m = Math.min(m + p, 1);
      const h = {
        inv_mass: m,
        opts: k,
        settled: !0,
        dt: (c - u) * 60 / 1e3
      }, q = Nl(h, r, t, a);
      return u = c, r = t, e.set(t = q), h.settled && (o = null), !h.settled;
    })), new Promise((c) => {
      o.promise.then(() => {
        w === s && c();
      });
    }));
  }
  const k = {
    set: j,
    update: (d, _) => j(d(a, t), _),
    subscribe: e.subscribe,
    stiffness: n,
    damping: i,
    precision: f
  };
  return k;
}
const {
  SvelteComponent: Vi,
  append: ie,
  attr: O,
  component_subscribe: lt,
  detach: Di,
  element: Bi,
  init: Ti,
  insert: Ui,
  noop: tt,
  safe_not_equal: Zi,
  set_style: tl,
  svg_element: se,
  toggle_class: nt
} = window.__gradio__svelte__internal, { onMount: Pi } = window.__gradio__svelte__internal;
function Ii(t) {
  let l, e, n, i, f, u, o, s, r, a, m, p;
  return {
    c() {
      l = Bi("div"), e = se("svg"), n = se("g"), i = se("path"), f = se("path"), u = se("path"), o = se("path"), s = se("g"), r = se("path"), a = se("path"), m = se("path"), p = se("path"), O(i, "d", "M255.926 0.754768L509.702 139.936V221.027L255.926 81.8465V0.754768Z"), O(i, "fill", "#FF7C00"), O(i, "fill-opacity", "0.4"), O(i, "class", "svelte-43sxxs"), O(f, "d", "M509.69 139.936L254.981 279.641V361.255L509.69 221.55V139.936Z"), O(f, "fill", "#FF7C00"), O(f, "class", "svelte-43sxxs"), O(u, "d", "M0.250138 139.937L254.981 279.641V361.255L0.250138 221.55V139.937Z"), O(u, "fill", "#FF7C00"), O(u, "fill-opacity", "0.4"), O(u, "class", "svelte-43sxxs"), O(o, "d", "M255.923 0.232622L0.236328 139.936V221.55L255.923 81.8469V0.232622Z"), O(o, "fill", "#FF7C00"), O(o, "class", "svelte-43sxxs"), tl(n, "transform", "translate(" + /*$top*/
      t[1][0] + "px, " + /*$top*/
      t[1][1] + "px)"), O(r, "d", "M255.926 141.5L509.702 280.681V361.773L255.926 222.592V141.5Z"), O(r, "fill", "#FF7C00"), O(r, "fill-opacity", "0.4"), O(r, "class", "svelte-43sxxs"), O(a, "d", "M509.69 280.679L254.981 420.384V501.998L509.69 362.293V280.679Z"), O(a, "fill", "#FF7C00"), O(a, "class", "svelte-43sxxs"), O(m, "d", "M0.250138 280.681L254.981 420.386V502L0.250138 362.295V280.681Z"), O(m, "fill", "#FF7C00"), O(m, "fill-opacity", "0.4"), O(m, "class", "svelte-43sxxs"), O(p, "d", "M255.923 140.977L0.236328 280.68V362.294L255.923 222.591V140.977Z"), O(p, "fill", "#FF7C00"), O(p, "class", "svelte-43sxxs"), tl(s, "transform", "translate(" + /*$bottom*/
      t[2][0] + "px, " + /*$bottom*/
      t[2][1] + "px)"), O(e, "viewBox", "-1200 -1200 3000 3000"), O(e, "fill", "none"), O(e, "xmlns", "http://www.w3.org/2000/svg"), O(e, "class", "svelte-43sxxs"), O(l, "class", "svelte-43sxxs"), nt(
        l,
        "margin",
        /*margin*/
        t[0]
      );
    },
    m(g, j) {
      Ui(g, l, j), ie(l, e), ie(e, n), ie(n, i), ie(n, f), ie(n, u), ie(n, o), ie(e, s), ie(s, r), ie(s, a), ie(s, m), ie(s, p);
    },
    p(g, [j]) {
      j & /*$top*/
      2 && tl(n, "transform", "translate(" + /*$top*/
      g[1][0] + "px, " + /*$top*/
      g[1][1] + "px)"), j & /*$bottom*/
      4 && tl(s, "transform", "translate(" + /*$bottom*/
      g[2][0] + "px, " + /*$bottom*/
      g[2][1] + "px)"), j & /*margin*/
      1 && nt(
        l,
        "margin",
        /*margin*/
        g[0]
      );
    },
    i: tt,
    o: tt,
    d(g) {
      g && Di(l);
    }
  };
}
function Hi(t, l, e) {
  let n, i;
  var f = this && this.__awaiter || function(g, j, k, d) {
    function _(w) {
      return w instanceof k ? w : new k(function(c) {
        c(w);
      });
    }
    return new (k || (k = Promise))(function(w, c) {
      function h(E) {
        try {
          v(d.next(E));
        } catch (C) {
          c(C);
        }
      }
      function q(E) {
        try {
          v(d.throw(E));
        } catch (C) {
          c(C);
        }
      }
      function v(E) {
        E.done ? w(E.value) : _(E.value).then(h, q);
      }
      v((d = d.apply(g, j || [])).next());
    });
  };
  let { margin: u = !0 } = l;
  const o = et([0, 0]);
  lt(t, o, (g) => e(1, n = g));
  const s = et([0, 0]);
  lt(t, s, (g) => e(2, i = g));
  let r;
  function a() {
    return f(this, void 0, void 0, function* () {
      yield Promise.all([o.set([125, 140]), s.set([-125, -140])]), yield Promise.all([o.set([-125, 140]), s.set([125, -140])]), yield Promise.all([o.set([-125, 0]), s.set([125, -0])]), yield Promise.all([o.set([125, 0]), s.set([-125, 0])]);
    });
  }
  function m() {
    return f(this, void 0, void 0, function* () {
      yield a(), r || m();
    });
  }
  function p() {
    return f(this, void 0, void 0, function* () {
      yield Promise.all([o.set([125, 0]), s.set([-125, 0])]), m();
    });
  }
  return Pi(() => (p(), () => r = !0)), t.$$set = (g) => {
    "margin" in g && e(0, u = g.margin);
  }, [u, n, i, o, s];
}
class Ji extends Vi {
  constructor(l) {
    super(), Ti(this, l, Hi, Ii, Zi, { margin: 0 });
  }
}
const {
  SvelteComponent: Ri,
  append: Fe,
  attr: _e,
  binding_callbacks: it,
  check_outros: xt,
  create_component: Xi,
  create_slot: Yi,
  destroy_component: Gi,
  destroy_each: $t,
  detach: M,
  element: ge,
  empty: Re,
  ensure_array_like: rl,
  get_all_dirty_from_scope: Ki,
  get_slot_changes: Qi,
  group_outros: en,
  init: Wi,
  insert: z,
  mount_component: xi,
  noop: Fl,
  safe_not_equal: $i,
  set_data: ne,
  set_style: qe,
  space: ce,
  text: B,
  toggle_class: te,
  transition_in: He,
  transition_out: Je,
  update_slot_base: es
} = window.__gradio__svelte__internal, { tick: ls } = window.__gradio__svelte__internal, { onDestroy: ts } = window.__gradio__svelte__internal, ns = (t) => ({}), st = (t) => ({});
function ot(t, l, e) {
  const n = t.slice();
  return n[39] = l[e], n[41] = e, n;
}
function ft(t, l, e) {
  const n = t.slice();
  return n[39] = l[e], n;
}
function is(t) {
  let l, e = (
    /*i18n*/
    t[1]("common.error") + ""
  ), n, i, f;
  const u = (
    /*#slots*/
    t[29].error
  ), o = Yi(
    u,
    t,
    /*$$scope*/
    t[28],
    st
  );
  return {
    c() {
      l = ge("span"), n = B(e), i = ce(), o && o.c(), _e(l, "class", "error svelte-1yserjw");
    },
    m(s, r) {
      z(s, l, r), Fe(l, n), z(s, i, r), o && o.m(s, r), f = !0;
    },
    p(s, r) {
      (!f || r[0] & /*i18n*/
      2) && e !== (e = /*i18n*/
      s[1]("common.error") + "") && ne(n, e), o && o.p && (!f || r[0] & /*$$scope*/
      268435456) && es(
        o,
        u,
        s,
        /*$$scope*/
        s[28],
        f ? Qi(
          u,
          /*$$scope*/
          s[28],
          r,
          ns
        ) : Ki(
          /*$$scope*/
          s[28]
        ),
        st
      );
    },
    i(s) {
      f || (He(o, s), f = !0);
    },
    o(s) {
      Je(o, s), f = !1;
    },
    d(s) {
      s && (M(l), M(i)), o && o.d(s);
    }
  };
}
function ss(t) {
  let l, e, n, i, f, u, o, s, r, a = (
    /*variant*/
    t[8] === "default" && /*show_eta_bar*/
    t[18] && /*show_progress*/
    t[6] === "full" && ut(t)
  );
  function m(c, h) {
    if (
      /*progress*/
      c[7]
    ) return us;
    if (
      /*queue_position*/
      c[2] !== null && /*queue_size*/
      c[3] !== void 0 && /*queue_position*/
      c[2] >= 0
    ) return fs;
    if (
      /*queue_position*/
      c[2] === 0
    ) return os;
  }
  let p = m(t), g = p && p(t), j = (
    /*timer*/
    t[5] && _t(t)
  );
  const k = [cs, _s], d = [];
  function _(c, h) {
    return (
      /*last_progress_level*/
      c[15] != null ? 0 : (
        /*show_progress*/
        c[6] === "full" ? 1 : -1
      )
    );
  }
  ~(f = _(t)) && (u = d[f] = k[f](t));
  let w = !/*timer*/
  t[5] && wt(t);
  return {
    c() {
      a && a.c(), l = ce(), e = ge("div"), g && g.c(), n = ce(), j && j.c(), i = ce(), u && u.c(), o = ce(), w && w.c(), s = Re(), _e(e, "class", "progress-text svelte-1yserjw"), te(
        e,
        "meta-text-center",
        /*variant*/
        t[8] === "center"
      ), te(
        e,
        "meta-text",
        /*variant*/
        t[8] === "default"
      );
    },
    m(c, h) {
      a && a.m(c, h), z(c, l, h), z(c, e, h), g && g.m(e, null), Fe(e, n), j && j.m(e, null), z(c, i, h), ~f && d[f].m(c, h), z(c, o, h), w && w.m(c, h), z(c, s, h), r = !0;
    },
    p(c, h) {
      /*variant*/
      c[8] === "default" && /*show_eta_bar*/
      c[18] && /*show_progress*/
      c[6] === "full" ? a ? a.p(c, h) : (a = ut(c), a.c(), a.m(l.parentNode, l)) : a && (a.d(1), a = null), p === (p = m(c)) && g ? g.p(c, h) : (g && g.d(1), g = p && p(c), g && (g.c(), g.m(e, n))), /*timer*/
      c[5] ? j ? j.p(c, h) : (j = _t(c), j.c(), j.m(e, null)) : j && (j.d(1), j = null), (!r || h[0] & /*variant*/
      256) && te(
        e,
        "meta-text-center",
        /*variant*/
        c[8] === "center"
      ), (!r || h[0] & /*variant*/
      256) && te(
        e,
        "meta-text",
        /*variant*/
        c[8] === "default"
      );
      let q = f;
      f = _(c), f === q ? ~f && d[f].p(c, h) : (u && (en(), Je(d[q], 1, 1, () => {
        d[q] = null;
      }), xt()), ~f ? (u = d[f], u ? u.p(c, h) : (u = d[f] = k[f](c), u.c()), He(u, 1), u.m(o.parentNode, o)) : u = null), /*timer*/
      c[5] ? w && (w.d(1), w = null) : w ? w.p(c, h) : (w = wt(c), w.c(), w.m(s.parentNode, s));
    },
    i(c) {
      r || (He(u), r = !0);
    },
    o(c) {
      Je(u), r = !1;
    },
    d(c) {
      c && (M(l), M(e), M(i), M(o), M(s)), a && a.d(c), g && g.d(), j && j.d(), ~f && d[f].d(c), w && w.d(c);
    }
  };
}
function ut(t) {
  let l, e = `translateX(${/*eta_level*/
  (t[17] || 0) * 100 - 100}%)`;
  return {
    c() {
      l = ge("div"), _e(l, "class", "eta-bar svelte-1yserjw"), qe(l, "transform", e);
    },
    m(n, i) {
      z(n, l, i);
    },
    p(n, i) {
      i[0] & /*eta_level*/
      131072 && e !== (e = `translateX(${/*eta_level*/
      (n[17] || 0) * 100 - 100}%)`) && qe(l, "transform", e);
    },
    d(n) {
      n && M(l);
    }
  };
}
function os(t) {
  let l;
  return {
    c() {
      l = B("processing |");
    },
    m(e, n) {
      z(e, l, n);
    },
    p: Fl,
    d(e) {
      e && M(l);
    }
  };
}
function fs(t) {
  let l, e = (
    /*queue_position*/
    t[2] + 1 + ""
  ), n, i, f, u;
  return {
    c() {
      l = B("queue: "), n = B(e), i = B("/"), f = B(
        /*queue_size*/
        t[3]
      ), u = B(" |");
    },
    m(o, s) {
      z(o, l, s), z(o, n, s), z(o, i, s), z(o, f, s), z(o, u, s);
    },
    p(o, s) {
      s[0] & /*queue_position*/
      4 && e !== (e = /*queue_position*/
      o[2] + 1 + "") && ne(n, e), s[0] & /*queue_size*/
      8 && ne(
        f,
        /*queue_size*/
        o[3]
      );
    },
    d(o) {
      o && (M(l), M(n), M(i), M(f), M(u));
    }
  };
}
function us(t) {
  let l, e = rl(
    /*progress*/
    t[7]
  ), n = [];
  for (let i = 0; i < e.length; i += 1)
    n[i] = at(ft(t, e, i));
  return {
    c() {
      for (let i = 0; i < n.length; i += 1)
        n[i].c();
      l = Re();
    },
    m(i, f) {
      for (let u = 0; u < n.length; u += 1)
        n[u] && n[u].m(i, f);
      z(i, l, f);
    },
    p(i, f) {
      if (f[0] & /*progress*/
      128) {
        e = rl(
          /*progress*/
          i[7]
        );
        let u;
        for (u = 0; u < e.length; u += 1) {
          const o = ft(i, e, u);
          n[u] ? n[u].p(o, f) : (n[u] = at(o), n[u].c(), n[u].m(l.parentNode, l));
        }
        for (; u < n.length; u += 1)
          n[u].d(1);
        n.length = e.length;
      }
    },
    d(i) {
      i && M(l), $t(n, i);
    }
  };
}
function rt(t) {
  let l, e = (
    /*p*/
    t[39].unit + ""
  ), n, i, f = " ", u;
  function o(a, m) {
    return (
      /*p*/
      a[39].length != null ? as : rs
    );
  }
  let s = o(t), r = s(t);
  return {
    c() {
      r.c(), l = ce(), n = B(e), i = B(" | "), u = B(f);
    },
    m(a, m) {
      r.m(a, m), z(a, l, m), z(a, n, m), z(a, i, m), z(a, u, m);
    },
    p(a, m) {
      s === (s = o(a)) && r ? r.p(a, m) : (r.d(1), r = s(a), r && (r.c(), r.m(l.parentNode, l))), m[0] & /*progress*/
      128 && e !== (e = /*p*/
      a[39].unit + "") && ne(n, e);
    },
    d(a) {
      a && (M(l), M(n), M(i), M(u)), r.d(a);
    }
  };
}
function rs(t) {
  let l = Ue(
    /*p*/
    t[39].index || 0
  ) + "", e;
  return {
    c() {
      e = B(l);
    },
    m(n, i) {
      z(n, e, i);
    },
    p(n, i) {
      i[0] & /*progress*/
      128 && l !== (l = Ue(
        /*p*/
        n[39].index || 0
      ) + "") && ne(e, l);
    },
    d(n) {
      n && M(e);
    }
  };
}
function as(t) {
  let l = Ue(
    /*p*/
    t[39].index || 0
  ) + "", e, n, i = Ue(
    /*p*/
    t[39].length
  ) + "", f;
  return {
    c() {
      e = B(l), n = B("/"), f = B(i);
    },
    m(u, o) {
      z(u, e, o), z(u, n, o), z(u, f, o);
    },
    p(u, o) {
      o[0] & /*progress*/
      128 && l !== (l = Ue(
        /*p*/
        u[39].index || 0
      ) + "") && ne(e, l), o[0] & /*progress*/
      128 && i !== (i = Ue(
        /*p*/
        u[39].length
      ) + "") && ne(f, i);
    },
    d(u) {
      u && (M(e), M(n), M(f));
    }
  };
}
function at(t) {
  let l, e = (
    /*p*/
    t[39].index != null && rt(t)
  );
  return {
    c() {
      e && e.c(), l = Re();
    },
    m(n, i) {
      e && e.m(n, i), z(n, l, i);
    },
    p(n, i) {
      /*p*/
      n[39].index != null ? e ? e.p(n, i) : (e = rt(n), e.c(), e.m(l.parentNode, l)) : e && (e.d(1), e = null);
    },
    d(n) {
      n && M(l), e && e.d(n);
    }
  };
}
function _t(t) {
  let l, e = (
    /*eta*/
    t[0] ? `/${/*formatted_eta*/
    t[19]}` : ""
  ), n, i;
  return {
    c() {
      l = B(
        /*formatted_timer*/
        t[20]
      ), n = B(e), i = B("s");
    },
    m(f, u) {
      z(f, l, u), z(f, n, u), z(f, i, u);
    },
    p(f, u) {
      u[0] & /*formatted_timer*/
      1048576 && ne(
        l,
        /*formatted_timer*/
        f[20]
      ), u[0] & /*eta, formatted_eta*/
      524289 && e !== (e = /*eta*/
      f[0] ? `/${/*formatted_eta*/
      f[19]}` : "") && ne(n, e);
    },
    d(f) {
      f && (M(l), M(n), M(i));
    }
  };
}
function _s(t) {
  let l, e;
  return l = new Ji({
    props: { margin: (
      /*variant*/
      t[8] === "default"
    ) }
  }), {
    c() {
      Xi(l.$$.fragment);
    },
    m(n, i) {
      xi(l, n, i), e = !0;
    },
    p(n, i) {
      const f = {};
      i[0] & /*variant*/
      256 && (f.margin = /*variant*/
      n[8] === "default"), l.$set(f);
    },
    i(n) {
      e || (He(l.$$.fragment, n), e = !0);
    },
    o(n) {
      Je(l.$$.fragment, n), e = !1;
    },
    d(n) {
      Gi(l, n);
    }
  };
}
function cs(t) {
  let l, e, n, i, f, u = `${/*last_progress_level*/
  t[15] * 100}%`, o = (
    /*progress*/
    t[7] != null && ct(t)
  );
  return {
    c() {
      l = ge("div"), e = ge("div"), o && o.c(), n = ce(), i = ge("div"), f = ge("div"), _e(e, "class", "progress-level-inner svelte-1yserjw"), _e(f, "class", "progress-bar svelte-1yserjw"), qe(f, "width", u), _e(i, "class", "progress-bar-wrap svelte-1yserjw"), _e(l, "class", "progress-level svelte-1yserjw");
    },
    m(s, r) {
      z(s, l, r), Fe(l, e), o && o.m(e, null), Fe(l, n), Fe(l, i), Fe(i, f), t[30](f);
    },
    p(s, r) {
      /*progress*/
      s[7] != null ? o ? o.p(s, r) : (o = ct(s), o.c(), o.m(e, null)) : o && (o.d(1), o = null), r[0] & /*last_progress_level*/
      32768 && u !== (u = `${/*last_progress_level*/
      s[15] * 100}%`) && qe(f, "width", u);
    },
    i: Fl,
    o: Fl,
    d(s) {
      s && M(l), o && o.d(), t[30](null);
    }
  };
}
function ct(t) {
  let l, e = rl(
    /*progress*/
    t[7]
  ), n = [];
  for (let i = 0; i < e.length; i += 1)
    n[i] = gt(ot(t, e, i));
  return {
    c() {
      for (let i = 0; i < n.length; i += 1)
        n[i].c();
      l = Re();
    },
    m(i, f) {
      for (let u = 0; u < n.length; u += 1)
        n[u] && n[u].m(i, f);
      z(i, l, f);
    },
    p(i, f) {
      if (f[0] & /*progress_level, progress*/
      16512) {
        e = rl(
          /*progress*/
          i[7]
        );
        let u;
        for (u = 0; u < e.length; u += 1) {
          const o = ot(i, e, u);
          n[u] ? n[u].p(o, f) : (n[u] = gt(o), n[u].c(), n[u].m(l.parentNode, l));
        }
        for (; u < n.length; u += 1)
          n[u].d(1);
        n.length = e.length;
      }
    },
    d(i) {
      i && M(l), $t(n, i);
    }
  };
}
function dt(t) {
  let l, e, n, i, f = (
    /*i*/
    t[41] !== 0 && ds()
  ), u = (
    /*p*/
    t[39].desc != null && mt(t)
  ), o = (
    /*p*/
    t[39].desc != null && /*progress_level*/
    t[14] && /*progress_level*/
    t[14][
      /*i*/
      t[41]
    ] != null && bt()
  ), s = (
    /*progress_level*/
    t[14] != null && ht(t)
  );
  return {
    c() {
      f && f.c(), l = ce(), u && u.c(), e = ce(), o && o.c(), n = ce(), s && s.c(), i = Re();
    },
    m(r, a) {
      f && f.m(r, a), z(r, l, a), u && u.m(r, a), z(r, e, a), o && o.m(r, a), z(r, n, a), s && s.m(r, a), z(r, i, a);
    },
    p(r, a) {
      /*p*/
      r[39].desc != null ? u ? u.p(r, a) : (u = mt(r), u.c(), u.m(e.parentNode, e)) : u && (u.d(1), u = null), /*p*/
      r[39].desc != null && /*progress_level*/
      r[14] && /*progress_level*/
      r[14][
        /*i*/
        r[41]
      ] != null ? o || (o = bt(), o.c(), o.m(n.parentNode, n)) : o && (o.d(1), o = null), /*progress_level*/
      r[14] != null ? s ? s.p(r, a) : (s = ht(r), s.c(), s.m(i.parentNode, i)) : s && (s.d(1), s = null);
    },
    d(r) {
      r && (M(l), M(e), M(n), M(i)), f && f.d(r), u && u.d(r), o && o.d(r), s && s.d(r);
    }
  };
}
function ds(t) {
  let l;
  return {
    c() {
      l = B(" /");
    },
    m(e, n) {
      z(e, l, n);
    },
    d(e) {
      e && M(l);
    }
  };
}
function mt(t) {
  let l = (
    /*p*/
    t[39].desc + ""
  ), e;
  return {
    c() {
      e = B(l);
    },
    m(n, i) {
      z(n, e, i);
    },
    p(n, i) {
      i[0] & /*progress*/
      128 && l !== (l = /*p*/
      n[39].desc + "") && ne(e, l);
    },
    d(n) {
      n && M(e);
    }
  };
}
function bt(t) {
  let l;
  return {
    c() {
      l = B("-");
    },
    m(e, n) {
      z(e, l, n);
    },
    d(e) {
      e && M(l);
    }
  };
}
function ht(t) {
  let l = (100 * /*progress_level*/
  (t[14][
    /*i*/
    t[41]
  ] || 0)).toFixed(1) + "", e, n;
  return {
    c() {
      e = B(l), n = B("%");
    },
    m(i, f) {
      z(i, e, f), z(i, n, f);
    },
    p(i, f) {
      f[0] & /*progress_level*/
      16384 && l !== (l = (100 * /*progress_level*/
      (i[14][
        /*i*/
        i[41]
      ] || 0)).toFixed(1) + "") && ne(e, l);
    },
    d(i) {
      i && (M(e), M(n));
    }
  };
}
function gt(t) {
  let l, e = (
    /*p*/
    (t[39].desc != null || /*progress_level*/
    t[14] && /*progress_level*/
    t[14][
      /*i*/
      t[41]
    ] != null) && dt(t)
  );
  return {
    c() {
      e && e.c(), l = Re();
    },
    m(n, i) {
      e && e.m(n, i), z(n, l, i);
    },
    p(n, i) {
      /*p*/
      n[39].desc != null || /*progress_level*/
      n[14] && /*progress_level*/
      n[14][
        /*i*/
        n[41]
      ] != null ? e ? e.p(n, i) : (e = dt(n), e.c(), e.m(l.parentNode, l)) : e && (e.d(1), e = null);
    },
    d(n) {
      n && M(l), e && e.d(n);
    }
  };
}
function wt(t) {
  let l, e;
  return {
    c() {
      l = ge("p"), e = B(
        /*loading_text*/
        t[9]
      ), _e(l, "class", "loading svelte-1yserjw");
    },
    m(n, i) {
      z(n, l, i), Fe(l, e);
    },
    p(n, i) {
      i[0] & /*loading_text*/
      512 && ne(
        e,
        /*loading_text*/
        n[9]
      );
    },
    d(n) {
      n && M(l);
    }
  };
}
function ms(t) {
  let l, e, n, i, f;
  const u = [ss, is], o = [];
  function s(r, a) {
    return (
      /*status*/
      r[4] === "pending" ? 0 : (
        /*status*/
        r[4] === "error" ? 1 : -1
      )
    );
  }
  return ~(e = s(t)) && (n = o[e] = u[e](t)), {
    c() {
      l = ge("div"), n && n.c(), _e(l, "class", i = "wrap " + /*variant*/
      t[8] + " " + /*show_progress*/
      t[6] + " svelte-1yserjw"), te(l, "hide", !/*status*/
      t[4] || /*status*/
      t[4] === "complete" || /*show_progress*/
      t[6] === "hidden"), te(
        l,
        "translucent",
        /*variant*/
        t[8] === "center" && /*status*/
        (t[4] === "pending" || /*status*/
        t[4] === "error") || /*translucent*/
        t[11] || /*show_progress*/
        t[6] === "minimal"
      ), te(
        l,
        "generating",
        /*status*/
        t[4] === "generating"
      ), te(
        l,
        "border",
        /*border*/
        t[12]
      ), qe(
        l,
        "position",
        /*absolute*/
        t[10] ? "absolute" : "static"
      ), qe(
        l,
        "padding",
        /*absolute*/
        t[10] ? "0" : "var(--size-8) 0"
      );
    },
    m(r, a) {
      z(r, l, a), ~e && o[e].m(l, null), t[31](l), f = !0;
    },
    p(r, a) {
      let m = e;
      e = s(r), e === m ? ~e && o[e].p(r, a) : (n && (en(), Je(o[m], 1, 1, () => {
        o[m] = null;
      }), xt()), ~e ? (n = o[e], n ? n.p(r, a) : (n = o[e] = u[e](r), n.c()), He(n, 1), n.m(l, null)) : n = null), (!f || a[0] & /*variant, show_progress*/
      320 && i !== (i = "wrap " + /*variant*/
      r[8] + " " + /*show_progress*/
      r[6] + " svelte-1yserjw")) && _e(l, "class", i), (!f || a[0] & /*variant, show_progress, status, show_progress*/
      336) && te(l, "hide", !/*status*/
      r[4] || /*status*/
      r[4] === "complete" || /*show_progress*/
      r[6] === "hidden"), (!f || a[0] & /*variant, show_progress, variant, status, translucent, show_progress*/
      2384) && te(
        l,
        "translucent",
        /*variant*/
        r[8] === "center" && /*status*/
        (r[4] === "pending" || /*status*/
        r[4] === "error") || /*translucent*/
        r[11] || /*show_progress*/
        r[6] === "minimal"
      ), (!f || a[0] & /*variant, show_progress, status*/
      336) && te(
        l,
        "generating",
        /*status*/
        r[4] === "generating"
      ), (!f || a[0] & /*variant, show_progress, border*/
      4416) && te(
        l,
        "border",
        /*border*/
        r[12]
      ), a[0] & /*absolute*/
      1024 && qe(
        l,
        "position",
        /*absolute*/
        r[10] ? "absolute" : "static"
      ), a[0] & /*absolute*/
      1024 && qe(
        l,
        "padding",
        /*absolute*/
        r[10] ? "0" : "var(--size-8) 0"
      );
    },
    i(r) {
      f || (He(n), f = !0);
    },
    o(r) {
      Je(n), f = !1;
    },
    d(r) {
      r && M(l), ~e && o[e].d(), t[31](null);
    }
  };
}
var bs = function(t, l, e, n) {
  function i(f) {
    return f instanceof e ? f : new e(function(u) {
      u(f);
    });
  }
  return new (e || (e = Promise))(function(f, u) {
    function o(a) {
      try {
        r(n.next(a));
      } catch (m) {
        u(m);
      }
    }
    function s(a) {
      try {
        r(n.throw(a));
      } catch (m) {
        u(m);
      }
    }
    function r(a) {
      a.done ? f(a.value) : i(a.value).then(o, s);
    }
    r((n = n.apply(t, l || [])).next());
  });
};
let nl = [], ql = !1;
function hs(t) {
  return bs(this, arguments, void 0, function* (l, e = !0) {
    if (!(window.__gradio_mode__ === "website" || window.__gradio_mode__ !== "app" && e !== !0)) {
      if (nl.push(l), !ql) ql = !0;
      else return;
      yield ls(), requestAnimationFrame(() => {
        let n = [0, 0];
        for (let i = 0; i < nl.length; i++) {
          const u = nl[i].getBoundingClientRect();
          (i === 0 || u.top + window.scrollY <= n[0]) && (n[0] = u.top + window.scrollY, n[1] = i);
        }
        window.scrollTo({ top: n[0] - 20, behavior: "smooth" }), ql = !1, nl = [];
      });
    }
  });
}
function gs(t, l, e) {
  let n, { $$slots: i = {}, $$scope: f } = l;
  this && this.__awaiter;
  let { i18n: u } = l, { eta: o = null } = l, { queue_position: s } = l, { queue_size: r } = l, { status: a } = l, { scroll_to_output: m = !1 } = l, { timer: p = !0 } = l, { show_progress: g = "full" } = l, { message: j = null } = l, { progress: k = null } = l, { variant: d = "default" } = l, { loading_text: _ = "Loading..." } = l, { absolute: w = !0 } = l, { translucent: c = !1 } = l, { border: h = !1 } = l, { autoscroll: q } = l, v, E = !1, C = 0, L = 0, T = null, P = null, le = 0, N = null, J, R = null, me = !0;
  const ke = () => {
    e(0, o = e(26, T = e(19, F = null))), e(24, C = performance.now()), e(25, L = 0), E = !0, ve();
  };
  function ve() {
    requestAnimationFrame(() => {
      e(25, L = (performance.now() - C) / 1e3), E && ve();
    });
  }
  function ye() {
    e(25, L = 0), e(0, o = e(26, T = e(19, F = null))), E && (E = !1);
  }
  ts(() => {
    E && ye();
  });
  let F = null;
  function y(S) {
    it[S ? "unshift" : "push"](() => {
      R = S, e(16, R), e(7, k), e(14, N), e(15, J);
    });
  }
  function Y(S) {
    it[S ? "unshift" : "push"](() => {
      v = S, e(13, v);
    });
  }
  return t.$$set = (S) => {
    "i18n" in S && e(1, u = S.i18n), "eta" in S && e(0, o = S.eta), "queue_position" in S && e(2, s = S.queue_position), "queue_size" in S && e(3, r = S.queue_size), "status" in S && e(4, a = S.status), "scroll_to_output" in S && e(21, m = S.scroll_to_output), "timer" in S && e(5, p = S.timer), "show_progress" in S && e(6, g = S.show_progress), "message" in S && e(22, j = S.message), "progress" in S && e(7, k = S.progress), "variant" in S && e(8, d = S.variant), "loading_text" in S && e(9, _ = S.loading_text), "absolute" in S && e(10, w = S.absolute), "translucent" in S && e(11, c = S.translucent), "border" in S && e(12, h = S.border), "autoscroll" in S && e(23, q = S.autoscroll), "$$scope" in S && e(28, f = S.$$scope);
  }, t.$$.update = () => {
    t.$$.dirty[0] & /*eta, old_eta, timer_start, eta_from_start*/
    218103809 && (o === null && e(0, o = T), o != null && T !== o && (e(27, P = (performance.now() - C) / 1e3 + o), e(19, F = P.toFixed(1)), e(26, T = o))), t.$$.dirty[0] & /*eta_from_start, timer_diff*/
    167772160 && e(17, le = P === null || P <= 0 || !L ? null : Math.min(L / P, 1)), t.$$.dirty[0] & /*progress*/
    128 && k != null && e(18, me = !1), t.$$.dirty[0] & /*progress, progress_level, progress_bar, last_progress_level*/
    114816 && (k != null ? e(14, N = k.map((S) => {
      if (S.index != null && S.length != null)
        return S.index / S.length;
      if (S.progress != null)
        return S.progress;
    })) : e(14, N = null), N ? (e(15, J = N[N.length - 1]), R && (J === 0 ? e(16, R.style.transition = "0", R) : e(16, R.style.transition = "150ms", R))) : e(15, J = void 0)), t.$$.dirty[0] & /*status*/
    16 && (a === "pending" ? ke() : ye()), t.$$.dirty[0] & /*el, scroll_to_output, status, autoscroll*/
    10493968 && v && m && (a === "pending" || a === "complete") && hs(v, q), t.$$.dirty[0] & /*status, message*/
    4194320, t.$$.dirty[0] & /*timer_diff*/
    33554432 && e(20, n = L.toFixed(1));
  }, [
    o,
    u,
    s,
    r,
    a,
    p,
    g,
    k,
    d,
    _,
    w,
    c,
    h,
    v,
    N,
    J,
    R,
    le,
    me,
    F,
    n,
    m,
    j,
    q,
    C,
    L,
    T,
    P,
    f,
    i,
    y,
    Y
  ];
}
class ws extends Ri {
  constructor(l) {
    super(), Wi(
      this,
      l,
      gs,
      ms,
      $i,
      {
        i18n: 1,
        eta: 0,
        queue_position: 2,
        queue_size: 3,
        status: 4,
        scroll_to_output: 21,
        timer: 5,
        show_progress: 6,
        message: 22,
        progress: 7,
        variant: 8,
        loading_text: 9,
        absolute: 10,
        translucent: 11,
        border: 12,
        autoscroll: 23
      },
      null,
      [-1, -1]
    );
  }
}
const {
  SvelteComponent: ps,
  append: ln,
  attr: D,
  bubble: ks,
  check_outros: vs,
  create_slot: tn,
  detach: el,
  element: hl,
  empty: ys,
  get_all_dirty_from_scope: nn,
  get_slot_changes: sn,
  group_outros: Cs,
  init: js,
  insert: ll,
  listen: qs,
  safe_not_equal: Ss,
  set_style: Q,
  space: on,
  src_url_equal: al,
  toggle_class: Ze,
  transition_in: _l,
  transition_out: cl,
  update_slot_base: fn
} = window.__gradio__svelte__internal;
function Es(t) {
  let l, e, n, i, f, u, o = (
    /*icon*/
    t[7] && pt(t)
  );
  const s = (
    /*#slots*/
    t[12].default
  ), r = tn(
    s,
    t,
    /*$$scope*/
    t[11],
    null
  );
  return {
    c() {
      l = hl("button"), o && o.c(), e = on(), r && r.c(), D(l, "class", n = /*size*/
      t[4] + " " + /*variant*/
      t[3] + " " + /*elem_classes*/
      t[1].join(" ") + " svelte-8huxfn"), D(
        l,
        "id",
        /*elem_id*/
        t[0]
      ), l.disabled = /*disabled*/
      t[8], Ze(l, "hidden", !/*visible*/
      t[2]), Q(
        l,
        "flex-grow",
        /*scale*/
        t[9]
      ), Q(
        l,
        "width",
        /*scale*/
        t[9] === 0 ? "fit-content" : null
      ), Q(l, "min-width", typeof /*min_width*/
      t[10] == "number" ? `calc(min(${/*min_width*/
      t[10]}px, 100%))` : null);
    },
    m(a, m) {
      ll(a, l, m), o && o.m(l, null), ln(l, e), r && r.m(l, null), i = !0, f || (u = qs(
        l,
        "click",
        /*click_handler*/
        t[13]
      ), f = !0);
    },
    p(a, m) {
      /*icon*/
      a[7] ? o ? o.p(a, m) : (o = pt(a), o.c(), o.m(l, e)) : o && (o.d(1), o = null), r && r.p && (!i || m & /*$$scope*/
      2048) && fn(
        r,
        s,
        a,
        /*$$scope*/
        a[11],
        i ? sn(
          s,
          /*$$scope*/
          a[11],
          m,
          null
        ) : nn(
          /*$$scope*/
          a[11]
        ),
        null
      ), (!i || m & /*size, variant, elem_classes*/
      26 && n !== (n = /*size*/
      a[4] + " " + /*variant*/
      a[3] + " " + /*elem_classes*/
      a[1].join(" ") + " svelte-8huxfn")) && D(l, "class", n), (!i || m & /*elem_id*/
      1) && D(
        l,
        "id",
        /*elem_id*/
        a[0]
      ), (!i || m & /*disabled*/
      256) && (l.disabled = /*disabled*/
      a[8]), (!i || m & /*size, variant, elem_classes, visible*/
      30) && Ze(l, "hidden", !/*visible*/
      a[2]), m & /*scale*/
      512 && Q(
        l,
        "flex-grow",
        /*scale*/
        a[9]
      ), m & /*scale*/
      512 && Q(
        l,
        "width",
        /*scale*/
        a[9] === 0 ? "fit-content" : null
      ), m & /*min_width*/
      1024 && Q(l, "min-width", typeof /*min_width*/
      a[10] == "number" ? `calc(min(${/*min_width*/
      a[10]}px, 100%))` : null);
    },
    i(a) {
      i || (_l(r, a), i = !0);
    },
    o(a) {
      cl(r, a), i = !1;
    },
    d(a) {
      a && el(l), o && o.d(), r && r.d(a), f = !1, u();
    }
  };
}
function Ns(t) {
  let l, e, n, i, f = (
    /*icon*/
    t[7] && kt(t)
  );
  const u = (
    /*#slots*/
    t[12].default
  ), o = tn(
    u,
    t,
    /*$$scope*/
    t[11],
    null
  );
  return {
    c() {
      l = hl("a"), f && f.c(), e = on(), o && o.c(), D(
        l,
        "href",
        /*link*/
        t[6]
      ), D(l, "rel", "noopener noreferrer"), D(
        l,
        "aria-disabled",
        /*disabled*/
        t[8]
      ), D(l, "class", n = /*size*/
      t[4] + " " + /*variant*/
      t[3] + " " + /*elem_classes*/
      t[1].join(" ") + " svelte-8huxfn"), D(
        l,
        "id",
        /*elem_id*/
        t[0]
      ), Ze(l, "hidden", !/*visible*/
      t[2]), Ze(
        l,
        "disabled",
        /*disabled*/
        t[8]
      ), Q(
        l,
        "flex-grow",
        /*scale*/
        t[9]
      ), Q(
        l,
        "pointer-events",
        /*disabled*/
        t[8] ? "none" : null
      ), Q(
        l,
        "width",
        /*scale*/
        t[9] === 0 ? "fit-content" : null
      ), Q(l, "min-width", typeof /*min_width*/
      t[10] == "number" ? `calc(min(${/*min_width*/
      t[10]}px, 100%))` : null);
    },
    m(s, r) {
      ll(s, l, r), f && f.m(l, null), ln(l, e), o && o.m(l, null), i = !0;
    },
    p(s, r) {
      /*icon*/
      s[7] ? f ? f.p(s, r) : (f = kt(s), f.c(), f.m(l, e)) : f && (f.d(1), f = null), o && o.p && (!i || r & /*$$scope*/
      2048) && fn(
        o,
        u,
        s,
        /*$$scope*/
        s[11],
        i ? sn(
          u,
          /*$$scope*/
          s[11],
          r,
          null
        ) : nn(
          /*$$scope*/
          s[11]
        ),
        null
      ), (!i || r & /*link*/
      64) && D(
        l,
        "href",
        /*link*/
        s[6]
      ), (!i || r & /*disabled*/
      256) && D(
        l,
        "aria-disabled",
        /*disabled*/
        s[8]
      ), (!i || r & /*size, variant, elem_classes*/
      26 && n !== (n = /*size*/
      s[4] + " " + /*variant*/
      s[3] + " " + /*elem_classes*/
      s[1].join(" ") + " svelte-8huxfn")) && D(l, "class", n), (!i || r & /*elem_id*/
      1) && D(
        l,
        "id",
        /*elem_id*/
        s[0]
      ), (!i || r & /*size, variant, elem_classes, visible*/
      30) && Ze(l, "hidden", !/*visible*/
      s[2]), (!i || r & /*size, variant, elem_classes, disabled*/
      282) && Ze(
        l,
        "disabled",
        /*disabled*/
        s[8]
      ), r & /*scale*/
      512 && Q(
        l,
        "flex-grow",
        /*scale*/
        s[9]
      ), r & /*disabled*/
      256 && Q(
        l,
        "pointer-events",
        /*disabled*/
        s[8] ? "none" : null
      ), r & /*scale*/
      512 && Q(
        l,
        "width",
        /*scale*/
        s[9] === 0 ? "fit-content" : null
      ), r & /*min_width*/
      1024 && Q(l, "min-width", typeof /*min_width*/
      s[10] == "number" ? `calc(min(${/*min_width*/
      s[10]}px, 100%))` : null);
    },
    i(s) {
      i || (_l(o, s), i = !0);
    },
    o(s) {
      cl(o, s), i = !1;
    },
    d(s) {
      s && el(l), f && f.d(), o && o.d(s);
    }
  };
}
function pt(t) {
  let l, e, n;
  return {
    c() {
      l = hl("img"), D(l, "class", "button-icon svelte-8huxfn"), al(l.src, e = /*icon*/
      t[7].url) || D(l, "src", e), D(l, "alt", n = `${/*value*/
      t[5]} icon`);
    },
    m(i, f) {
      ll(i, l, f);
    },
    p(i, f) {
      f & /*icon*/
      128 && !al(l.src, e = /*icon*/
      i[7].url) && D(l, "src", e), f & /*value*/
      32 && n !== (n = `${/*value*/
      i[5]} icon`) && D(l, "alt", n);
    },
    d(i) {
      i && el(l);
    }
  };
}
function kt(t) {
  let l, e, n;
  return {
    c() {
      l = hl("img"), D(l, "class", "button-icon svelte-8huxfn"), al(l.src, e = /*icon*/
      t[7].url) || D(l, "src", e), D(l, "alt", n = `${/*value*/
      t[5]} icon`);
    },
    m(i, f) {
      ll(i, l, f);
    },
    p(i, f) {
      f & /*icon*/
      128 && !al(l.src, e = /*icon*/
      i[7].url) && D(l, "src", e), f & /*value*/
      32 && n !== (n = `${/*value*/
      i[5]} icon`) && D(l, "alt", n);
    },
    d(i) {
      i && el(l);
    }
  };
}
function Fs(t) {
  let l, e, n, i;
  const f = [Ns, Es], u = [];
  function o(s, r) {
    return (
      /*link*/
      s[6] && /*link*/
      s[6].length > 0 ? 0 : 1
    );
  }
  return l = o(t), e = u[l] = f[l](t), {
    c() {
      e.c(), n = ys();
    },
    m(s, r) {
      u[l].m(s, r), ll(s, n, r), i = !0;
    },
    p(s, [r]) {
      let a = l;
      l = o(s), l === a ? u[l].p(s, r) : (Cs(), cl(u[a], 1, 1, () => {
        u[a] = null;
      }), vs(), e = u[l], e ? e.p(s, r) : (e = u[l] = f[l](s), e.c()), _l(e, 1), e.m(n.parentNode, n));
    },
    i(s) {
      i || (_l(e), i = !0);
    },
    o(s) {
      cl(e), i = !1;
    },
    d(s) {
      s && el(n), u[l].d(s);
    }
  };
}
function Ls(t, l, e) {
  let { $$slots: n = {}, $$scope: i } = l, { elem_id: f = "" } = l, { elem_classes: u = [] } = l, { visible: o = !0 } = l, { variant: s = "secondary" } = l, { size: r = "lg" } = l, { value: a = null } = l, { link: m = null } = l, { icon: p = null } = l, { disabled: g = !1 } = l, { scale: j = null } = l, { min_width: k = void 0 } = l;
  function d(_) {
    ks.call(this, t, _);
  }
  return t.$$set = (_) => {
    "elem_id" in _ && e(0, f = _.elem_id), "elem_classes" in _ && e(1, u = _.elem_classes), "visible" in _ && e(2, o = _.visible), "variant" in _ && e(3, s = _.variant), "size" in _ && e(4, r = _.size), "value" in _ && e(5, a = _.value), "link" in _ && e(6, m = _.link), "icon" in _ && e(7, p = _.icon), "disabled" in _ && e(8, g = _.disabled), "scale" in _ && e(9, j = _.scale), "min_width" in _ && e(10, k = _.min_width), "$$scope" in _ && e(11, i = _.$$scope);
  }, [
    f,
    u,
    o,
    s,
    r,
    a,
    m,
    p,
    g,
    j,
    k,
    i,
    n,
    d
  ];
}
class Ms extends ps {
  constructor(l) {
    super(), js(this, l, Ls, Fs, Ss, {
      elem_id: 0,
      elem_classes: 1,
      visible: 2,
      variant: 3,
      size: 4,
      value: 5,
      link: 6,
      icon: 7,
      disabled: 8,
      scale: 9,
      min_width: 10
    });
  }
}
const {
  SvelteComponent: zs,
  add_render_callback: un,
  append: il,
  attr: $,
  binding_callbacks: vt,
  check_outros: Os,
  create_bidirectional_transition: yt,
  destroy_each: As,
  detach: Ke,
  element: dl,
  empty: Vs,
  ensure_array_like: Ct,
  group_outros: Ds,
  init: Bs,
  insert: Qe,
  listen: Ll,
  prevent_default: Ts,
  run_all: Us,
  safe_not_equal: Zs,
  set_data: Ps,
  set_style: je,
  space: Ml,
  text: Is,
  toggle_class: fe,
  transition_in: Sl,
  transition_out: jt
} = window.__gradio__svelte__internal, { createEventDispatcher: Hs } = window.__gradio__svelte__internal;
function qt(t, l, e) {
  const n = t.slice();
  return n[26] = l[e], n;
}
function St(t) {
  let l, e, n, i, f, u = Ct(
    /*filtered_indices*/
    t[1]
  ), o = [];
  for (let s = 0; s < u.length; s += 1)
    o[s] = Et(qt(t, u, s));
  return {
    c() {
      l = dl("ul");
      for (let s = 0; s < o.length; s += 1)
        o[s].c();
      $(l, "class", "options svelte-yuohum"), $(l, "role", "listbox"), je(
        l,
        "top",
        /*top*/
        t[9]
      ), je(
        l,
        "bottom",
        /*bottom*/
        t[10]
      ), je(l, "max-height", `calc(${/*max_height*/
      t[11]}px - var(--window-padding))`), je(
        l,
        "width",
        /*input_width*/
        t[8] + "px"
      );
    },
    m(s, r) {
      Qe(s, l, r);
      for (let a = 0; a < o.length; a += 1)
        o[a] && o[a].m(l, null);
      t[23](l), n = !0, i || (f = Ll(l, "mousedown", Ts(
        /*mousedown_handler*/
        t[22]
      )), i = !0);
    },
    p(s, r) {
      if (r & /*filtered_indices, choices, selected_indices, active_index*/
      51) {
        u = Ct(
          /*filtered_indices*/
          s[1]
        );
        let a;
        for (a = 0; a < u.length; a += 1) {
          const m = qt(s, u, a);
          o[a] ? o[a].p(m, r) : (o[a] = Et(m), o[a].c(), o[a].m(l, null));
        }
        for (; a < o.length; a += 1)
          o[a].d(1);
        o.length = u.length;
      }
      r & /*top*/
      512 && je(
        l,
        "top",
        /*top*/
        s[9]
      ), r & /*bottom*/
      1024 && je(
        l,
        "bottom",
        /*bottom*/
        s[10]
      ), r & /*max_height*/
      2048 && je(l, "max-height", `calc(${/*max_height*/
      s[11]}px - var(--window-padding))`), r & /*input_width*/
      256 && je(
        l,
        "width",
        /*input_width*/
        s[8] + "px"
      );
    },
    i(s) {
      n || (s && un(() => {
        n && (e || (e = yt(l, xl, { duration: 200, y: 5 }, !0)), e.run(1));
      }), n = !0);
    },
    o(s) {
      s && (e || (e = yt(l, xl, { duration: 200, y: 5 }, !1)), e.run(0)), n = !1;
    },
    d(s) {
      s && Ke(l), As(o, s), t[23](null), s && e && e.end(), i = !1, f();
    }
  };
}
function Et(t) {
  let l, e, n, i = (
    /*choices*/
    t[0][
      /*index*/
      t[26]
    ][0] + ""
  ), f, u, o, s, r;
  return {
    c() {
      l = dl("li"), e = dl("span"), e.textContent = "✓", n = Ml(), f = Is(i), u = Ml(), $(e, "class", "inner-item svelte-yuohum"), fe(e, "hide", !/*selected_indices*/
      t[4].includes(
        /*index*/
        t[26]
      )), $(l, "class", "item svelte-yuohum"), $(l, "data-index", o = /*index*/
      t[26]), $(l, "aria-label", s = /*choices*/
      t[0][
        /*index*/
        t[26]
      ][0]), $(l, "data-testid", "dropdown-option"), $(l, "role", "option"), $(l, "aria-selected", r = /*selected_indices*/
      t[4].includes(
        /*index*/
        t[26]
      )), fe(
        l,
        "selected",
        /*selected_indices*/
        t[4].includes(
          /*index*/
          t[26]
        )
      ), fe(
        l,
        "active",
        /*index*/
        t[26] === /*active_index*/
        t[5]
      ), fe(
        l,
        "bg-gray-100",
        /*index*/
        t[26] === /*active_index*/
        t[5]
      ), fe(
        l,
        "dark:bg-gray-600",
        /*index*/
        t[26] === /*active_index*/
        t[5]
      );
    },
    m(a, m) {
      Qe(a, l, m), il(l, e), il(l, n), il(l, f), il(l, u);
    },
    p(a, m) {
      m & /*selected_indices, filtered_indices*/
      18 && fe(e, "hide", !/*selected_indices*/
      a[4].includes(
        /*index*/
        a[26]
      )), m & /*choices, filtered_indices*/
      3 && i !== (i = /*choices*/
      a[0][
        /*index*/
        a[26]
      ][0] + "") && Ps(f, i), m & /*filtered_indices*/
      2 && o !== (o = /*index*/
      a[26]) && $(l, "data-index", o), m & /*choices, filtered_indices*/
      3 && s !== (s = /*choices*/
      a[0][
        /*index*/
        a[26]
      ][0]) && $(l, "aria-label", s), m & /*selected_indices, filtered_indices*/
      18 && r !== (r = /*selected_indices*/
      a[4].includes(
        /*index*/
        a[26]
      )) && $(l, "aria-selected", r), m & /*selected_indices, filtered_indices*/
      18 && fe(
        l,
        "selected",
        /*selected_indices*/
        a[4].includes(
          /*index*/
          a[26]
        )
      ), m & /*filtered_indices, active_index*/
      34 && fe(
        l,
        "active",
        /*index*/
        a[26] === /*active_index*/
        a[5]
      ), m & /*filtered_indices, active_index*/
      34 && fe(
        l,
        "bg-gray-100",
        /*index*/
        a[26] === /*active_index*/
        a[5]
      ), m & /*filtered_indices, active_index*/
      34 && fe(
        l,
        "dark:bg-gray-600",
        /*index*/
        a[26] === /*active_index*/
        a[5]
      );
    },
    d(a) {
      a && Ke(l);
    }
  };
}
function Js(t) {
  let l, e, n, i, f;
  un(
    /*onwindowresize*/
    t[20]
  );
  let u = (
    /*show_options*/
    t[2] && !/*disabled*/
    t[3] && St(t)
  );
  return {
    c() {
      l = dl("div"), e = Ml(), u && u.c(), n = Vs(), $(l, "class", "reference");
    },
    m(o, s) {
      Qe(o, l, s), t[21](l), Qe(o, e, s), u && u.m(o, s), Qe(o, n, s), i || (f = [
        Ll(
          window,
          "scroll",
          /*scroll_listener*/
          t[13]
        ),
        Ll(
          window,
          "resize",
          /*onwindowresize*/
          t[20]
        )
      ], i = !0);
    },
    p(o, [s]) {
      /*show_options*/
      o[2] && !/*disabled*/
      o[3] ? u ? (u.p(o, s), s & /*show_options, disabled*/
      12 && Sl(u, 1)) : (u = St(o), u.c(), Sl(u, 1), u.m(n.parentNode, n)) : u && (Ds(), jt(u, 1, 1, () => {
        u = null;
      }), Os());
    },
    i(o) {
      Sl(u);
    },
    o(o) {
      jt(u);
    },
    d(o) {
      o && (Ke(l), Ke(e), Ke(n)), t[21](null), u && u.d(o), i = !1, Us(f);
    }
  };
}
function Rs(t, l, e) {
  var n, i;
  let { choices: f } = l, { filtered_indices: u } = l, { show_options: o = !1 } = l, { disabled: s = !1 } = l, { selected_indices: r = [] } = l, { active_index: a = null } = l, m, p, g, j, k, d, _, w, c, h;
  function q() {
    const { top: N, bottom: J } = k.getBoundingClientRect();
    e(17, m = N), e(18, p = h - J);
  }
  let v = null;
  function E() {
    o && (v !== null && clearTimeout(v), v = setTimeout(
      () => {
        q(), v = null;
      },
      10
    ));
  }
  const C = Hs();
  function L() {
    e(12, h = window.innerHeight);
  }
  function T(N) {
    vt[N ? "unshift" : "push"](() => {
      k = N, e(6, k);
    });
  }
  const P = (N) => C("change", N);
  function le(N) {
    vt[N ? "unshift" : "push"](() => {
      d = N, e(7, d);
    });
  }
  return t.$$set = (N) => {
    "choices" in N && e(0, f = N.choices), "filtered_indices" in N && e(1, u = N.filtered_indices), "show_options" in N && e(2, o = N.show_options), "disabled" in N && e(3, s = N.disabled), "selected_indices" in N && e(4, r = N.selected_indices), "active_index" in N && e(5, a = N.active_index);
  }, t.$$.update = () => {
    if (t.$$.dirty & /*show_options, refElement, listElement, selected_indices, _a, _b, distance_from_bottom, distance_from_top, input_height*/
    1016020) {
      if (o && k) {
        if (d && r.length > 0) {
          let J = d.querySelectorAll("li");
          for (const R of Array.from(J))
            if (R.getAttribute("data-index") === r[0].toString()) {
              e(15, n = d?.scrollTo) === null || n === void 0 || n.call(d, 0, R.offsetTop);
              break;
            }
        }
        q();
        const N = e(16, i = k.parentElement) === null || i === void 0 ? void 0 : i.getBoundingClientRect();
        e(19, g = N?.height || 0), e(8, j = N?.width || 0);
      }
      p > m ? (e(9, _ = `${m}px`), e(11, c = p), e(10, w = null)) : (e(10, w = `${p + g}px`), e(11, c = m - g), e(9, _ = null));
    }
  }, [
    f,
    u,
    o,
    s,
    r,
    a,
    k,
    d,
    j,
    _,
    w,
    c,
    h,
    E,
    C,
    n,
    i,
    m,
    p,
    g,
    L,
    T,
    P,
    le
  ];
}
class rn extends zs {
  constructor(l) {
    super(), Bs(this, l, Rs, Js, Zs, {
      choices: 0,
      filtered_indices: 1,
      show_options: 2,
      disabled: 3,
      selected_indices: 4,
      active_index: 5
    });
  }
}
function Xs(t, l) {
  return (t % l + l) % l;
}
function zl(t, l) {
  return t.reduce((e, n, i) => ((!l || n[0].toLowerCase().includes(l.toLowerCase())) && e.push(i), e), []);
}
function an(t, l, e) {
  t("change", l), e || t("input");
}
function _n(t, l, e) {
  if (t.key === "Escape")
    return [!1, l];
  if ((t.key === "ArrowDown" || t.key === "ArrowUp") && e.length >= 0)
    if (l === null)
      l = t.key === "ArrowDown" ? e[0] : e[e.length - 1];
    else {
      const n = e.indexOf(l), i = t.key === "ArrowUp" ? -1 : 1;
      l = e[Xs(n + i, e.length)];
    }
  return [!0, l];
}
function Ol(t) {
  const l = /* @__PURE__ */ new Map();
  if (!t)
    return l;
  for (const e in t)
    t.hasOwnProperty(e) && (typeof t[e] == "object" && t[e] !== null ? l.set(e, Ol(t[e])) : l.set(e, t[e]));
  return l;
}
function cn(t) {
  return Object.fromEntries(
    Array.from(
      t.entries(),
      ([e, n]) => n instanceof Map ? [e, cn(n)] : [e, n]
    )
  );
}
const {
  SvelteComponent: Ys,
  append: Ne,
  attr: x,
  binding_callbacks: Gs,
  check_outros: Ks,
  create_component: Al,
  destroy_component: Vl,
  detach: Ul,
  element: Be,
  group_outros: Qs,
  init: Ws,
  insert: Zl,
  listen: Xe,
  mount_component: Dl,
  run_all: xs,
  safe_not_equal: $s,
  set_data: eo,
  set_input_value: Nt,
  space: El,
  text: lo,
  toggle_class: Oe,
  transition_in: Te,
  transition_out: Ge
} = window.__gradio__svelte__internal, { createEventDispatcher: to, afterUpdate: no } = window.__gradio__svelte__internal;
function io(t) {
  let l;
  return {
    c() {
      l = lo(
        /*label*/
        t[0]
      );
    },
    m(e, n) {
      Zl(e, l, n);
    },
    p(e, n) {
      n[0] & /*label*/
      1 && eo(
        l,
        /*label*/
        e[0]
      );
    },
    d(e) {
      e && Ul(l);
    }
  };
}
function Ft(t) {
  let l, e, n;
  return e = new Yt({}), {
    c() {
      l = Be("div"), Al(e.$$.fragment), x(l, "class", "icon-wrap svelte-1m1zvyj");
    },
    m(i, f) {
      Zl(i, l, f), Dl(e, l, null), n = !0;
    },
    i(i) {
      n || (Te(e.$$.fragment, i), n = !0);
    },
    o(i) {
      Ge(e.$$.fragment, i), n = !1;
    },
    d(i) {
      i && Ul(l), Vl(e);
    }
  };
}
function so(t) {
  let l, e, n, i, f, u, o, s, r, a, m, p, g, j;
  e = new Xt({
    props: {
      show_label: (
        /*show_label*/
        t[4]
      ),
      info: (
        /*info*/
        t[1]
      ),
      $$slots: { default: [io] },
      $$scope: { ctx: t }
    }
  });
  let k = !/*disabled*/
  t[3] && Ft();
  return m = new rn({
    props: {
      show_options: (
        /*show_options*/
        t[12]
      ),
      choices: (
        /*choices*/
        t[2]
      ),
      filtered_indices: (
        /*filtered_indices*/
        t[10]
      ),
      disabled: (
        /*disabled*/
        t[3]
      ),
      selected_indices: (
        /*selected_index*/
        t[11] === null ? [] : [
          /*selected_index*/
          t[11]
        ]
      ),
      active_index: (
        /*active_index*/
        t[14]
      )
    }
  }), m.$on(
    "change",
    /*handle_option_selected*/
    t[16]
  ), {
    c() {
      l = Be("div"), Al(e.$$.fragment), n = El(), i = Be("div"), f = Be("div"), u = Be("div"), o = Be("input"), r = El(), k && k.c(), a = El(), Al(m.$$.fragment), x(o, "role", "listbox"), x(o, "aria-controls", "dropdown-options"), x(
        o,
        "aria-expanded",
        /*show_options*/
        t[12]
      ), x(
        o,
        "aria-label",
        /*label*/
        t[0]
      ), x(o, "class", "border-none svelte-1m1zvyj"), o.disabled = /*disabled*/
      t[3], x(o, "autocomplete", "off"), o.readOnly = s = !/*filterable*/
      t[7], Oe(o, "subdued", !/*choices_names*/
      t[13].includes(
        /*input_text*/
        t[9]
      ) && !/*allow_custom_value*/
      t[6]), x(u, "class", "secondary-wrap svelte-1m1zvyj"), x(f, "class", "wrap-inner svelte-1m1zvyj"), Oe(
        f,
        "show_options",
        /*show_options*/
        t[12]
      ), x(i, "class", "wrap svelte-1m1zvyj"), x(l, "class", "svelte-1m1zvyj"), Oe(
        l,
        "container",
        /*container*/
        t[5]
      );
    },
    m(d, _) {
      Zl(d, l, _), Dl(e, l, null), Ne(l, n), Ne(l, i), Ne(i, f), Ne(f, u), Ne(u, o), Nt(
        o,
        /*input_text*/
        t[9]
      ), t[29](o), Ne(u, r), k && k.m(u, null), Ne(i, a), Dl(m, i, null), p = !0, g || (j = [
        Xe(
          o,
          "input",
          /*input_input_handler*/
          t[28]
        ),
        Xe(
          o,
          "keydown",
          /*handle_key_down*/
          t[19]
        ),
        Xe(
          o,
          "keyup",
          /*keyup_handler*/
          t[30]
        ),
        Xe(
          o,
          "blur",
          /*handle_blur*/
          t[18]
        ),
        Xe(
          o,
          "focus",
          /*handle_focus*/
          t[17]
        )
      ], g = !0);
    },
    p(d, _) {
      const w = {};
      _[0] & /*show_label*/
      16 && (w.show_label = /*show_label*/
      d[4]), _[0] & /*info*/
      2 && (w.info = /*info*/
      d[1]), _[0] & /*label*/
      1 | _[1] & /*$$scope*/
      4 && (w.$$scope = { dirty: _, ctx: d }), e.$set(w), (!p || _[0] & /*show_options*/
      4096) && x(
        o,
        "aria-expanded",
        /*show_options*/
        d[12]
      ), (!p || _[0] & /*label*/
      1) && x(
        o,
        "aria-label",
        /*label*/
        d[0]
      ), (!p || _[0] & /*disabled*/
      8) && (o.disabled = /*disabled*/
      d[3]), (!p || _[0] & /*filterable*/
      128 && s !== (s = !/*filterable*/
      d[7])) && (o.readOnly = s), _[0] & /*input_text*/
      512 && o.value !== /*input_text*/
      d[9] && Nt(
        o,
        /*input_text*/
        d[9]
      ), (!p || _[0] & /*choices_names, input_text, allow_custom_value*/
      8768) && Oe(o, "subdued", !/*choices_names*/
      d[13].includes(
        /*input_text*/
        d[9]
      ) && !/*allow_custom_value*/
      d[6]), /*disabled*/
      d[3] ? k && (Qs(), Ge(k, 1, 1, () => {
        k = null;
      }), Ks()) : k ? _[0] & /*disabled*/
      8 && Te(k, 1) : (k = Ft(), k.c(), Te(k, 1), k.m(u, null)), (!p || _[0] & /*show_options*/
      4096) && Oe(
        f,
        "show_options",
        /*show_options*/
        d[12]
      );
      const c = {};
      _[0] & /*show_options*/
      4096 && (c.show_options = /*show_options*/
      d[12]), _[0] & /*choices*/
      4 && (c.choices = /*choices*/
      d[2]), _[0] & /*filtered_indices*/
      1024 && (c.filtered_indices = /*filtered_indices*/
      d[10]), _[0] & /*disabled*/
      8 && (c.disabled = /*disabled*/
      d[3]), _[0] & /*selected_index*/
      2048 && (c.selected_indices = /*selected_index*/
      d[11] === null ? [] : [
        /*selected_index*/
        d[11]
      ]), _[0] & /*active_index*/
      16384 && (c.active_index = /*active_index*/
      d[14]), m.$set(c), (!p || _[0] & /*container*/
      32) && Oe(
        l,
        "container",
        /*container*/
        d[5]
      );
    },
    i(d) {
      p || (Te(e.$$.fragment, d), Te(k), Te(m.$$.fragment, d), p = !0);
    },
    o(d) {
      Ge(e.$$.fragment, d), Ge(k), Ge(m.$$.fragment, d), p = !1;
    },
    d(d) {
      d && Ul(l), Vl(e), t[29](null), k && k.d(), Vl(m), g = !1, xs(j);
    }
  };
}
function oo(t, l, e) {
  let { label: n } = l, { info: i = void 0 } = l, { value: f = void 0 } = l, u, { value_is_output: o = !1 } = l, { choices: s } = l, r, { disabled: a = !1 } = l, { show_label: m } = l, { container: p = !0 } = l, { allow_custom_value: g = !1 } = l, { filterable: j = !0 } = l, k, d = !1, _, w, c = "", h = "", q = !1, v = [], E = null, C = null, L;
  const T = to();
  f && (L = s.map((F) => F[1]).indexOf(f), C = L, C === -1 ? (u = f, C = null) : ([c, u] = s[C], h = c), le());
  function P() {
    e(13, _ = s.map((F) => F[0])), e(24, w = s.map((F) => F[1]));
  }
  function le() {
    P(), f === void 0 ? (e(9, c = ""), e(11, C = null)) : w.includes(f) ? (e(9, c = _[w.indexOf(f)]), e(11, C = w.indexOf(f))) : g ? (e(9, c = f), e(11, C = null)) : (e(9, c = ""), e(11, C = null)), e(27, L = C);
  }
  function N(F) {
    if (e(11, C = parseInt(F.detail.target.dataset.index)), isNaN(C)) {
      e(11, C = null);
      return;
    }
    e(12, d = !1), e(14, E = null), k.blur();
  }
  function J(F) {
    e(10, v = s.map((y, Y) => Y)), e(12, d = !0), T("focus");
  }
  function R() {
    g ? e(20, f = c) : e(9, c = _[w.indexOf(f)]), e(12, d = !1), e(14, E = null), T("blur");
  }
  function me(F) {
    e(12, [d, E] = _n(F, E, v), d, (e(14, E), e(2, s), e(23, r), e(6, g), e(9, c), e(10, v), e(8, k), e(25, h), e(11, C), e(27, L), e(26, q), e(24, w))), F.key === "Enter" && (E !== null ? (e(11, C = E), e(12, d = !1), k.blur(), e(14, E = null)) : _.includes(c) ? (e(11, C = _.indexOf(c)), e(12, d = !1), e(14, E = null), k.blur()) : g && (e(20, f = c), e(11, C = null), e(12, d = !1), e(14, E = null), k.blur()));
  }
  no(() => {
    e(21, o = !1), e(26, q = !0);
  });
  function ke() {
    c = this.value, e(9, c), e(11, C), e(27, L), e(26, q), e(2, s), e(24, w);
  }
  function ve(F) {
    Gs[F ? "unshift" : "push"](() => {
      k = F, e(8, k);
    });
  }
  const ye = (F) => T("key_up", { key: F.key, input_value: c });
  return t.$$set = (F) => {
    "label" in F && e(0, n = F.label), "info" in F && e(1, i = F.info), "value" in F && e(20, f = F.value), "value_is_output" in F && e(21, o = F.value_is_output), "choices" in F && e(2, s = F.choices), "disabled" in F && e(3, a = F.disabled), "show_label" in F && e(4, m = F.show_label), "container" in F && e(5, p = F.container), "allow_custom_value" in F && e(6, g = F.allow_custom_value), "filterable" in F && e(7, j = F.filterable);
  }, t.$$.update = () => {
    t.$$.dirty[0] & /*selected_index, old_selected_index, initialized, choices, choices_values*/
    218105860 && C !== L && C !== null && q && (e(9, [c, f] = s[C], c, (e(20, f), e(11, C), e(27, L), e(26, q), e(2, s), e(24, w))), e(27, L = C), T("select", {
      index: C,
      value: w[C],
      selected: !0
    })), t.$$.dirty[0] & /*value, old_value, value_is_output*/
    7340032 && f != u && (le(), an(T, f, o), e(22, u = f)), t.$$.dirty[0] & /*choices*/
    4 && P(), t.$$.dirty[0] & /*choices, old_choices, allow_custom_value, input_text, filtered_indices, filter_input*/
    8390468 && s !== r && (g || le(), e(23, r = s), e(10, v = zl(s, c)), !g && v.length > 0 && e(14, E = v[0]), k == document.activeElement && e(12, d = !0)), t.$$.dirty[0] & /*input_text, old_input_text, choices, allow_custom_value, filtered_indices*/
    33556036 && c !== h && (e(10, v = zl(s, c)), e(25, h = c), !g && v.length > 0 && e(14, E = v[0]));
  }, [
    n,
    i,
    s,
    a,
    m,
    p,
    g,
    j,
    k,
    c,
    v,
    C,
    d,
    _,
    E,
    T,
    N,
    J,
    R,
    me,
    f,
    o,
    u,
    r,
    w,
    h,
    q,
    L,
    ke,
    ve,
    ye
  ];
}
class fo extends Ys {
  constructor(l) {
    super(), Ws(
      this,
      l,
      oo,
      so,
      $s,
      {
        label: 0,
        info: 1,
        value: 20,
        value_is_output: 21,
        choices: 2,
        disabled: 3,
        show_label: 4,
        container: 5,
        allow_custom_value: 6,
        filterable: 7
      },
      null,
      [-1, -1]
    );
  }
}
class uo {
  constructor({
    name: l,
    token: e,
    param_specs: n
  }) {
    this.name = l, this.token = e, this.param_specs = n || new Object();
  }
}
const {
  SvelteComponent: ro,
  attr: ao,
  detach: _o,
  element: co,
  init: mo,
  insert: bo,
  noop: Lt,
  safe_not_equal: ho,
  toggle_class: Ae
} = window.__gradio__svelte__internal;
function go(t) {
  let l;
  return {
    c() {
      l = co("div"), l.textContent = `${/*names_string*/
      t[2]}`, ao(l, "class", "svelte-1gecy8w"), Ae(
        l,
        "table",
        /*type*/
        t[0] === "table"
      ), Ae(
        l,
        "gallery",
        /*type*/
        t[0] === "gallery"
      ), Ae(
        l,
        "selected",
        /*selected*/
        t[1]
      );
    },
    m(e, n) {
      bo(e, l, n);
    },
    p(e, [n]) {
      n & /*type*/
      1 && Ae(
        l,
        "table",
        /*type*/
        e[0] === "table"
      ), n & /*type*/
      1 && Ae(
        l,
        "gallery",
        /*type*/
        e[0] === "gallery"
      ), n & /*selected*/
      2 && Ae(
        l,
        "selected",
        /*selected*/
        e[1]
      );
    },
    i: Lt,
    o: Lt,
    d(e) {
      e && _o(l);
    }
  };
}
function wo(t, l, e) {
  let { value: n } = l, { type: i } = l, { selected: f = !1 } = l, { choices: u } = l, r = (n ? Array.isArray(n) ? n : [n] : []).map((a) => {
    var m;
    return (m = u.find((p) => p[1] === a)) === null || m === void 0 ? void 0 : m[0];
  }).filter((a) => a !== void 0).join(", ");
  return t.$$set = (a) => {
    "value" in a && e(3, n = a.value), "type" in a && e(0, i = a.type), "selected" in a && e(1, f = a.selected), "choices" in a && e(4, u = a.choices);
  }, [i, f, r, n, u];
}
class Go extends ro {
  constructor(l) {
    super(), mo(this, l, wo, go, ho, {
      value: 3,
      type: 0,
      selected: 1,
      choices: 4
    });
  }
}
const {
  SvelteComponent: po,
  append: ue,
  attr: H,
  binding_callbacks: ko,
  check_outros: ml,
  create_component: We,
  destroy_component: xe,
  destroy_each: vo,
  detach: we,
  element: re,
  ensure_array_like: Mt,
  group_outros: bl,
  init: yo,
  insert: pe,
  listen: be,
  mount_component: $e,
  prevent_default: zt,
  run_all: Pl,
  safe_not_equal: Co,
  set_data: Il,
  set_input_value: Ot,
  space: Pe,
  text: Hl,
  toggle_class: Ve,
  transition_in: X,
  transition_out: ee
} = window.__gradio__svelte__internal, { afterUpdate: jo, createEventDispatcher: qo } = window.__gradio__svelte__internal;
function At(t, l, e) {
  const n = t.slice();
  return n[40] = l[e], n;
}
function So(t) {
  let l;
  return {
    c() {
      l = Hl(
        /*label*/
        t[0]
      );
    },
    m(e, n) {
      pe(e, l, n);
    },
    p(e, n) {
      n[0] & /*label*/
      1 && Il(
        l,
        /*label*/
        e[0]
      );
    },
    d(e) {
      e && we(l);
    }
  };
}
function Eo(t) {
  let l = (
    /*s*/
    t[40] + ""
  ), e;
  return {
    c() {
      e = Hl(l);
    },
    m(n, i) {
      pe(n, e, i);
    },
    p(n, i) {
      i[0] & /*selected_indices*/
      4096 && l !== (l = /*s*/
      n[40] + "") && Il(e, l);
    },
    d(n) {
      n && we(e);
    }
  };
}
function No(t) {
  let l = (
    /*choices_names*/
    t[15][
      /*s*/
      t[40]
    ] + ""
  ), e;
  return {
    c() {
      e = Hl(l);
    },
    m(n, i) {
      pe(n, e, i);
    },
    p(n, i) {
      i[0] & /*choices_names, selected_indices*/
      36864 && l !== (l = /*choices_names*/
      n[15][
        /*s*/
        n[40]
      ] + "") && Il(e, l);
    },
    d(n) {
      n && we(e);
    }
  };
}
function Vt(t) {
  let l, e, n, i, f, u;
  e = new Gt({});
  function o() {
    return (
      /*click_handler*/
      t[31](
        /*s*/
        t[40]
      )
    );
  }
  function s(...r) {
    return (
      /*keydown_handler*/
      t[32](
        /*s*/
        t[40],
        ...r
      )
    );
  }
  return {
    c() {
      l = re("div"), We(e.$$.fragment), H(l, "class", "token-remove svelte-xtjjyg"), H(l, "role", "button"), H(l, "tabindex", "0"), H(l, "title", n = /*i18n*/
      t[9]("common.remove") + " " + /*s*/
      t[40]);
    },
    m(r, a) {
      pe(r, l, a), $e(e, l, null), i = !0, f || (u = [
        be(l, "click", zt(o)),
        be(l, "keydown", zt(s))
      ], f = !0);
    },
    p(r, a) {
      t = r, (!i || a[0] & /*i18n, selected_indices*/
      4608 && n !== (n = /*i18n*/
      t[9]("common.remove") + " " + /*s*/
      t[40])) && H(l, "title", n);
    },
    i(r) {
      i || (X(e.$$.fragment, r), i = !0);
    },
    o(r) {
      ee(e.$$.fragment, r), i = !1;
    },
    d(r) {
      r && we(l), xe(e), f = !1, Pl(u);
    }
  };
}
function Dt(t) {
  let l, e, n, i;
  function f(r, a) {
    return typeof /*s*/
    r[40] == "number" ? No : Eo;
  }
  let u = f(t), o = u(t), s = !/*disabled*/
  t[4] && Vt(t);
  return {
    c() {
      l = re("div"), e = re("span"), o.c(), n = Pe(), s && s.c(), H(e, "class", "svelte-xtjjyg"), H(l, "class", "token svelte-xtjjyg");
    },
    m(r, a) {
      pe(r, l, a), ue(l, e), o.m(e, null), ue(l, n), s && s.m(l, null), i = !0;
    },
    p(r, a) {
      u === (u = f(r)) && o ? o.p(r, a) : (o.d(1), o = u(r), o && (o.c(), o.m(e, null))), /*disabled*/
      r[4] ? s && (bl(), ee(s, 1, 1, () => {
        s = null;
      }), ml()) : s ? (s.p(r, a), a[0] & /*disabled*/
      16 && X(s, 1)) : (s = Vt(r), s.c(), X(s, 1), s.m(l, null));
    },
    i(r) {
      i || (X(s), i = !0);
    },
    o(r) {
      ee(s), i = !1;
    },
    d(r) {
      r && we(l), o.d(), s && s.d();
    }
  };
}
function Bt(t) {
  let l, e, n, i, f = (
    /*selected_indices*/
    t[12].length > 0 && Tt(t)
  );
  return n = new Yt({}), {
    c() {
      f && f.c(), l = Pe(), e = re("span"), We(n.$$.fragment), H(e, "class", "icon-wrap svelte-xtjjyg");
    },
    m(u, o) {
      f && f.m(u, o), pe(u, l, o), pe(u, e, o), $e(n, e, null), i = !0;
    },
    p(u, o) {
      /*selected_indices*/
      u[12].length > 0 ? f ? (f.p(u, o), o[0] & /*selected_indices*/
      4096 && X(f, 1)) : (f = Tt(u), f.c(), X(f, 1), f.m(l.parentNode, l)) : f && (bl(), ee(f, 1, 1, () => {
        f = null;
      }), ml());
    },
    i(u) {
      i || (X(f), X(n.$$.fragment, u), i = !0);
    },
    o(u) {
      ee(f), ee(n.$$.fragment, u), i = !1;
    },
    d(u) {
      u && (we(l), we(e)), f && f.d(u), xe(n);
    }
  };
}
function Tt(t) {
  let l, e, n, i, f, u;
  return e = new Gt({}), {
    c() {
      l = re("div"), We(e.$$.fragment), H(l, "role", "button"), H(l, "tabindex", "0"), H(l, "class", "token-remove remove-all svelte-xtjjyg"), H(l, "title", n = /*i18n*/
      t[9]("common.clear"));
    },
    m(o, s) {
      pe(o, l, s), $e(e, l, null), i = !0, f || (u = [
        be(
          l,
          "click",
          /*remove_all*/
          t[21]
        ),
        be(
          l,
          "keydown",
          /*keydown_handler_1*/
          t[36]
        )
      ], f = !0);
    },
    p(o, s) {
      (!i || s[0] & /*i18n*/
      512 && n !== (n = /*i18n*/
      o[9]("common.clear"))) && H(l, "title", n);
    },
    i(o) {
      i || (X(e.$$.fragment, o), i = !0);
    },
    o(o) {
      ee(e.$$.fragment, o), i = !1;
    },
    d(o) {
      o && we(l), xe(e), f = !1, Pl(u);
    }
  };
}
function Fo(t) {
  let l, e, n, i, f, u, o, s, r, a, m, p, g, j, k;
  e = new Xt({
    props: {
      show_label: (
        /*show_label*/
        t[5]
      ),
      info: (
        /*info*/
        t[1]
      ),
      $$slots: { default: [So] },
      $$scope: { ctx: t }
    }
  });
  let d = Mt(
    /*selected_indices*/
    t[12]
  ), _ = [];
  for (let h = 0; h < d.length; h += 1)
    _[h] = Dt(At(t, d, h));
  const w = (h) => ee(_[h], 1, 1, () => {
    _[h] = null;
  });
  let c = !/*disabled*/
  t[4] && Bt(t);
  return p = new rn({
    props: {
      show_options: (
        /*show_options*/
        t[14]
      ),
      choices: (
        /*choices*/
        t[3]
      ),
      filtered_indices: (
        /*filtered_indices*/
        t[11]
      ),
      disabled: (
        /*disabled*/
        t[4]
      ),
      selected_indices: (
        /*selected_indices*/
        t[12]
      ),
      active_index: (
        /*active_index*/
        t[16]
      )
    }
  }), p.$on(
    "change",
    /*handle_option_selected*/
    t[20]
  ), {
    c() {
      l = re("label"), We(e.$$.fragment), n = Pe(), i = re("div"), f = re("div");
      for (let h = 0; h < _.length; h += 1)
        _[h].c();
      u = Pe(), o = re("div"), s = re("input"), a = Pe(), c && c.c(), m = Pe(), We(p.$$.fragment), H(s, "class", "border-none svelte-xtjjyg"), s.disabled = /*disabled*/
      t[4], H(s, "autocomplete", "off"), s.readOnly = r = !/*filterable*/
      t[8], Ve(s, "subdued", !/*choices_names*/
      t[15].includes(
        /*input_text*/
        t[10]
      ) && !/*allow_custom_value*/
      t[7] || /*selected_indices*/
      t[12].length === /*max_choices*/
      t[2]), H(o, "class", "secondary-wrap svelte-xtjjyg"), H(f, "class", "wrap-inner svelte-xtjjyg"), Ve(
        f,
        "show_options",
        /*show_options*/
        t[14]
      ), H(i, "class", "wrap svelte-xtjjyg"), H(l, "class", "svelte-xtjjyg"), Ve(
        l,
        "container",
        /*container*/
        t[6]
      );
    },
    m(h, q) {
      pe(h, l, q), $e(e, l, null), ue(l, n), ue(l, i), ue(i, f);
      for (let v = 0; v < _.length; v += 1)
        _[v] && _[v].m(f, null);
      ue(f, u), ue(f, o), ue(o, s), Ot(
        s,
        /*input_text*/
        t[10]
      ), t[34](s), ue(o, a), c && c.m(o, null), ue(i, m), $e(p, i, null), g = !0, j || (k = [
        be(
          s,
          "input",
          /*input_input_handler*/
          t[33]
        ),
        be(
          s,
          "keydown",
          /*handle_key_down*/
          t[23]
        ),
        be(
          s,
          "keyup",
          /*keyup_handler*/
          t[35]
        ),
        be(
          s,
          "blur",
          /*handle_blur*/
          t[18]
        ),
        be(
          s,
          "focus",
          /*handle_focus*/
          t[22]
        )
      ], j = !0);
    },
    p(h, q) {
      const v = {};
      if (q[0] & /*show_label*/
      32 && (v.show_label = /*show_label*/
      h[5]), q[0] & /*info*/
      2 && (v.info = /*info*/
      h[1]), q[0] & /*label*/
      1 | q[1] & /*$$scope*/
      4096 && (v.$$scope = { dirty: q, ctx: h }), e.$set(v), q[0] & /*i18n, selected_indices, remove_selected_choice, disabled, choices_names*/
      561680) {
        d = Mt(
          /*selected_indices*/
          h[12]
        );
        let C;
        for (C = 0; C < d.length; C += 1) {
          const L = At(h, d, C);
          _[C] ? (_[C].p(L, q), X(_[C], 1)) : (_[C] = Dt(L), _[C].c(), X(_[C], 1), _[C].m(f, u));
        }
        for (bl(), C = d.length; C < _.length; C += 1)
          w(C);
        ml();
      }
      (!g || q[0] & /*disabled*/
      16) && (s.disabled = /*disabled*/
      h[4]), (!g || q[0] & /*filterable*/
      256 && r !== (r = !/*filterable*/
      h[8])) && (s.readOnly = r), q[0] & /*input_text*/
      1024 && s.value !== /*input_text*/
      h[10] && Ot(
        s,
        /*input_text*/
        h[10]
      ), (!g || q[0] & /*choices_names, input_text, allow_custom_value, selected_indices, max_choices*/
      38020) && Ve(s, "subdued", !/*choices_names*/
      h[15].includes(
        /*input_text*/
        h[10]
      ) && !/*allow_custom_value*/
      h[7] || /*selected_indices*/
      h[12].length === /*max_choices*/
      h[2]), /*disabled*/
      h[4] ? c && (bl(), ee(c, 1, 1, () => {
        c = null;
      }), ml()) : c ? (c.p(h, q), q[0] & /*disabled*/
      16 && X(c, 1)) : (c = Bt(h), c.c(), X(c, 1), c.m(o, null)), (!g || q[0] & /*show_options*/
      16384) && Ve(
        f,
        "show_options",
        /*show_options*/
        h[14]
      );
      const E = {};
      q[0] & /*show_options*/
      16384 && (E.show_options = /*show_options*/
      h[14]), q[0] & /*choices*/
      8 && (E.choices = /*choices*/
      h[3]), q[0] & /*filtered_indices*/
      2048 && (E.filtered_indices = /*filtered_indices*/
      h[11]), q[0] & /*disabled*/
      16 && (E.disabled = /*disabled*/
      h[4]), q[0] & /*selected_indices*/
      4096 && (E.selected_indices = /*selected_indices*/
      h[12]), q[0] & /*active_index*/
      65536 && (E.active_index = /*active_index*/
      h[16]), p.$set(E), (!g || q[0] & /*container*/
      64) && Ve(
        l,
        "container",
        /*container*/
        h[6]
      );
    },
    i(h) {
      if (!g) {
        X(e.$$.fragment, h);
        for (let q = 0; q < d.length; q += 1)
          X(_[q]);
        X(c), X(p.$$.fragment, h), g = !0;
      }
    },
    o(h) {
      ee(e.$$.fragment, h), _ = _.filter(Boolean);
      for (let q = 0; q < _.length; q += 1)
        ee(_[q]);
      ee(c), ee(p.$$.fragment, h), g = !1;
    },
    d(h) {
      h && we(l), xe(e), vo(_, h), t[34](null), c && c.d(), xe(p), j = !1, Pl(k);
    }
  };
}
function Lo(t, l, e) {
  let { label: n } = l, { info: i = void 0 } = l, { value: f = [] } = l, u = [], { value_is_output: o = !1 } = l, { max_choices: s = null } = l, { choices: r } = l, a, { disabled: m = !1 } = l, { show_label: p } = l, { container: g = !0 } = l, { allow_custom_value: j = !1 } = l, { filterable: k = !0 } = l, { i18n: d } = l, _, w = "", c = "", h = !1, q, v, E = [], C = null, L = [], T = [];
  const P = qo();
  Array.isArray(f) && f.forEach((b) => {
    const U = r.map((oe) => oe[1]).indexOf(b);
    U !== -1 ? L.push(U) : L.push(b);
  });
  function le() {
    j || e(10, w = ""), j && w !== "" && (J(w), e(10, w = "")), e(14, h = !1), e(16, C = null), P("blur");
  }
  function N(b) {
    e(12, L = L.filter((U) => U !== b)), P("select", {
      index: typeof b == "number" ? b : -1,
      value: typeof b == "number" ? v[b] : b,
      selected: !1
    });
  }
  function J(b) {
    (s === null || L.length < s) && (e(12, L = [...L, b]), P("select", {
      index: typeof b == "number" ? b : -1,
      value: typeof b == "number" ? v[b] : b,
      selected: !0
    })), L.length === s && (e(14, h = !1), e(16, C = null), _.blur());
  }
  function R(b) {
    const U = parseInt(b.detail.target.dataset.index);
    me(U);
  }
  function me(b) {
    L.includes(b) ? N(b) : J(b), e(10, w = "");
  }
  function ke(b) {
    e(12, L = []), e(10, w = ""), b.preventDefault();
  }
  function ve(b) {
    e(11, E = r.map((U, oe) => oe)), (s === null || L.length < s) && e(14, h = !0), P("focus");
  }
  function ye(b) {
    e(14, [h, C] = _n(b, C, E), h, (e(16, C), e(3, r), e(27, a), e(10, w), e(28, c), e(7, j), e(11, E))), b.key === "Enter" && (C !== null ? me(C) : j && (J(w), e(10, w = ""))), b.key === "Backspace" && w === "" && e(12, L = [...L.slice(0, -1)]), L.length === s && (e(14, h = !1), e(16, C = null));
  }
  function F() {
    f === void 0 ? e(12, L = []) : Array.isArray(f) && e(12, L = f.map((b) => {
      const U = v.indexOf(b);
      if (U !== -1)
        return U;
      if (j)
        return b;
    }).filter((b) => b !== void 0));
  }
  jo(() => {
    e(25, o = !1);
  });
  const y = (b) => N(b), Y = (b, U) => {
    U.key === "Enter" && N(b);
  };
  function S() {
    w = this.value, e(10, w);
  }
  function V(b) {
    ko[b ? "unshift" : "push"](() => {
      _ = b, e(13, _);
    });
  }
  const I = (b) => P("key_up", { key: b.key, input_value: w }), A = (b) => {
    b.key === "Enter" && ke(b);
  };
  return t.$$set = (b) => {
    "label" in b && e(0, n = b.label), "info" in b && e(1, i = b.info), "value" in b && e(24, f = b.value), "value_is_output" in b && e(25, o = b.value_is_output), "max_choices" in b && e(2, s = b.max_choices), "choices" in b && e(3, r = b.choices), "disabled" in b && e(4, m = b.disabled), "show_label" in b && e(5, p = b.show_label), "container" in b && e(6, g = b.container), "allow_custom_value" in b && e(7, j = b.allow_custom_value), "filterable" in b && e(8, k = b.filterable), "i18n" in b && e(9, d = b.i18n);
  }, t.$$.update = () => {
    t.$$.dirty[0] & /*choices*/
    8 && (e(15, q = r.map((b) => b[0])), e(29, v = r.map((b) => b[1]))), t.$$.dirty[0] & /*choices, old_choices, input_text, old_input_text, allow_custom_value, filtered_indices*/
    402656392 && (r !== a || w !== c) && (e(11, E = zl(r, w)), e(27, a = r), e(28, c = w), j || e(16, C = E[0])), t.$$.dirty[0] & /*selected_indices, old_selected_index, choices_values*/
    1610616832 && JSON.stringify(L) != JSON.stringify(T) && (e(24, f = L.map((b) => typeof b == "number" ? v[b] : b)), e(30, T = L.slice())), t.$$.dirty[0] & /*value, old_value, value_is_output*/
    117440512 && JSON.stringify(f) != JSON.stringify(u) && (an(P, f, o), e(26, u = Array.isArray(f) ? f.slice() : f)), t.$$.dirty[0] & /*value*/
    16777216 && F();
  }, [
    n,
    i,
    s,
    r,
    m,
    p,
    g,
    j,
    k,
    d,
    w,
    E,
    L,
    _,
    h,
    q,
    C,
    P,
    le,
    N,
    R,
    ke,
    ve,
    ye,
    f,
    o,
    u,
    a,
    c,
    v,
    T,
    y,
    Y,
    S,
    V,
    I,
    A
  ];
}
class Ko extends po {
  constructor(l) {
    super(), yo(
      this,
      l,
      Lo,
      Fo,
      Co,
      {
        label: 0,
        info: 1,
        value: 24,
        value_is_output: 25,
        max_choices: 2,
        choices: 3,
        disabled: 4,
        show_label: 5,
        container: 6,
        allow_custom_value: 7,
        filterable: 8,
        i18n: 9
      },
      null,
      [-1, -1]
    );
  }
}
const {
  SvelteComponent: Mo,
  add_flush_callback: zo,
  append: De,
  assign: Oo,
  attr: Z,
  bind: Ao,
  binding_callbacks: Vo,
  check_outros: dn,
  create_component: gl,
  destroy_component: wl,
  detach: G,
  element: ae,
  empty: mn,
  get_spread_object: Do,
  get_spread_update: Bo,
  group_outros: bn,
  init: To,
  insert: K,
  listen: Bl,
  mount_component: pl,
  run_all: Uo,
  safe_not_equal: Zo,
  set_input_value: Ut,
  space: he,
  text: Po,
  transition_in: de,
  transition_out: Se
} = window.__gradio__svelte__internal, { onMount: Io } = window.__gradio__svelte__internal;
function Zt(t) {
  let l, e, n, i, f, u, o, s, r, a, m, p = (
    /*show_token_textbox*/
    t[10] && Pt(t)
  );
  function g(_) {
    t[21](_);
  }
  let j = {
    choices: (
      /*pipelines*/
      t[7]
    ),
    label: "",
    info: (
      /*info*/
      t[3]
    ),
    show_label: (
      /*show_label*/
      t[9]
    ),
    container: (
      /*container*/
      t[12]
    ),
    value: (
      /*default_pipeline*/
      t[8]
    ),
    disabled: !/*interactive*/
    t[17]
  };
  /*value_is_output*/
  t[2] !== void 0 && (j.value_is_output = /*value_is_output*/
  t[2]), i = new fo({ props: j }), Vo.push(() => Ao(i, "value_is_output", g)), i.$on(
    "input",
    /*input_handler*/
    t[22]
  ), i.$on(
    "select",
    /*select_handler*/
    t[23]
  ), i.$on(
    "blur",
    /*blur_handler*/
    t[24]
  ), i.$on(
    "focus",
    /*focus_handler*/
    t[25]
  ), i.$on(
    "key_up",
    /*key_up_handler*/
    t[26]
  );
  let k = (
    /*enable_edition*/
    t[11] && It(t)
  ), d = (
    /*value*/
    t[0].name !== "" && Ht(t)
  );
  return {
    c() {
      p && p.c(), l = he(), e = ae("p"), e.innerHTML = 'Select the <a href="https://huggingface.co/pyannote" class="svelte-hyoir0">pipeline</a> to use:', n = he(), gl(i.$$.fragment), u = he(), k && k.c(), o = he(), s = ae("div"), r = he(), d && d.c(), a = mn(), Z(e, "id", "dropdown-label"), Z(e, "class", "svelte-hyoir0"), Z(s, "class", "params-control svelte-hyoir0"), Z(s, "id", "params-control");
    },
    m(_, w) {
      p && p.m(_, w), K(_, l, w), K(_, e, w), K(_, n, w), pl(i, _, w), K(_, u, w), k && k.m(_, w), K(_, o, w), K(_, s, w), K(_, r, w), d && d.m(_, w), K(_, a, w), m = !0;
    },
    p(_, w) {
      /*show_token_textbox*/
      _[10] ? p ? p.p(_, w) : (p = Pt(_), p.c(), p.m(l.parentNode, l)) : p && (p.d(1), p = null);
      const c = {};
      w[0] & /*pipelines*/
      128 && (c.choices = /*pipelines*/
      _[7]), w[0] & /*info*/
      8 && (c.info = /*info*/
      _[3]), w[0] & /*show_label*/
      512 && (c.show_label = /*show_label*/
      _[9]), w[0] & /*container*/
      4096 && (c.container = /*container*/
      _[12]), w[0] & /*default_pipeline*/
      256 && (c.value = /*default_pipeline*/
      _[8]), w[0] & /*interactive*/
      131072 && (c.disabled = !/*interactive*/
      _[17]), !f && w[0] & /*value_is_output*/
      4 && (f = !0, c.value_is_output = /*value_is_output*/
      _[2], zo(() => f = !1)), i.$set(c), /*enable_edition*/
      _[11] ? k ? k.p(_, w) : (k = It(_), k.c(), k.m(o.parentNode, o)) : k && (k.d(1), k = null), /*value*/
      _[0].name !== "" ? d ? (d.p(_, w), w[0] & /*value*/
      1 && de(d, 1)) : (d = Ht(_), d.c(), de(d, 1), d.m(a.parentNode, a)) : d && (bn(), Se(d, 1, 1, () => {
        d = null;
      }), dn());
    },
    i(_) {
      m || (de(i.$$.fragment, _), de(d), m = !0);
    },
    o(_) {
      Se(i.$$.fragment, _), Se(d), m = !1;
    },
    d(_) {
      _ && (G(l), G(e), G(n), G(u), G(o), G(s), G(r), G(a)), p && p.d(_), wl(i, _), k && k.d(_), d && d.d(_);
    }
  };
}
function Pt(t) {
  let l, e, n, i, f, u;
  return {
    c() {
      l = ae("label"), l.textContent = "Enter your Hugging Face token:", e = he(), n = ae("input"), Z(l, "for", "token"), Z(l, "class", "label svelte-hyoir0"), Z(n, "data-testid", "textbox"), Z(n, "type", "text"), Z(n, "class", "text-area svelte-hyoir0"), Z(n, "name", "token"), Z(n, "id", "token"), Z(n, "placeholder", "hf_xxxxxxx..."), Z(n, "aria-label", "Enter your Hugging Face token"), Z(n, "maxlength", "50"), n.disabled = i = !/*interactive*/
      t[17];
    },
    m(o, s) {
      K(o, l, s), K(o, e, s), K(o, n, s), Ut(
        n,
        /*value*/
        t[0].token
      ), f || (u = Bl(
        n,
        "input",
        /*input_input_handler*/
        t[20]
      ), f = !0);
    },
    p(o, s) {
      s[0] & /*interactive*/
      131072 && i !== (i = !/*interactive*/
      o[17]) && (n.disabled = i), s[0] & /*value*/
      1 && n.value !== /*value*/
      o[0].token && Ut(
        n,
        /*value*/
        o[0].token
      );
    },
    d(o) {
      o && (G(l), G(e), G(n)), f = !1, u();
    }
  };
}
function It(t) {
  let l, e, n, i, f, u, o, s, r, a, m;
  return {
    c() {
      l = ae("div"), e = ae("p"), e.textContent = "Show configuration", n = he(), i = ae("label"), f = ae("input"), o = he(), s = ae("span"), Z(f, "type", "checkbox"), f.disabled = u = /*value*/
      t[0].name == "", Z(f, "class", "svelte-hyoir0"), Z(s, "class", "slider round svelte-hyoir0"), Z(i, "class", "switch svelte-hyoir0"), Z(i, "title", r = /*value*/
      t[0].name == "" ? "Please select a pipeline first" : "Show pipeline config"), Z(l, "class", "toggle-config svelte-hyoir0");
    },
    m(p, g) {
      K(p, l, g), De(l, e), De(l, n), De(l, i), De(i, f), f.checked = /*show_config*/
      t[1], De(i, o), De(i, s), a || (m = [
        Bl(
          f,
          "change",
          /*input_change_handler*/
          t[27]
        ),
        Bl(
          f,
          "input",
          /*input_handler_1*/
          t[28]
        )
      ], a = !0);
    },
    p(p, g) {
      g[0] & /*value*/
      1 && u !== (u = /*value*/
      p[0].name == "") && (f.disabled = u), g[0] & /*show_config*/
      2 && (f.checked = /*show_config*/
      p[1]), g[0] & /*value*/
      1 && r !== (r = /*value*/
      p[0].name == "" ? "Please select a pipeline first" : "Show pipeline config") && Z(i, "title", r);
    },
    d(p) {
      p && G(l), a = !1, Uo(m);
    }
  };
}
function Ht(t) {
  let l, e, n;
  return e = new Ms({
    props: {
      elem_id: (
        /*elem_id*/
        t[4]
      ),
      elem_classes: (
        /*elem_classes*/
        t[5]
      ),
      scale: (
        /*scale*/
        t[13]
      ),
      min_width: (
        /*min_width*/
        t[14]
      ),
      visible: (
        /*show_config*/
        t[1]
      ),
      $$slots: { default: [Ho] },
      $$scope: { ctx: t }
    }
  }), e.$on(
    "click",
    /*click_handler*/
    t[29]
  ), {
    c() {
      l = ae("div"), gl(e.$$.fragment), Z(l, "class", "validation svelte-hyoir0");
    },
    m(i, f) {
      K(i, l, f), pl(e, l, null), n = !0;
    },
    p(i, f) {
      const u = {};
      f[0] & /*elem_id*/
      16 && (u.elem_id = /*elem_id*/
      i[4]), f[0] & /*elem_classes*/
      32 && (u.elem_classes = /*elem_classes*/
      i[5]), f[0] & /*scale*/
      8192 && (u.scale = /*scale*/
      i[13]), f[0] & /*min_width*/
      16384 && (u.min_width = /*min_width*/
      i[14]), f[0] & /*show_config*/
      2 && (u.visible = /*show_config*/
      i[1]), f[1] & /*$$scope*/
      8 && (u.$$scope = { dirty: f, ctx: i }), e.$set(u);
    },
    i(i) {
      n || (de(e.$$.fragment, i), n = !0);
    },
    o(i) {
      Se(e.$$.fragment, i), n = !1;
    },
    d(i) {
      i && G(l), wl(e);
    }
  };
}
function Ho(t) {
  let l;
  return {
    c() {
      l = Po("Update parameters");
    },
    m(e, n) {
      K(e, l, n);
    },
    d(e) {
      e && G(l);
    }
  };
}
function Jo(t) {
  let l, e, n, i;
  const f = [
    {
      autoscroll: (
        /*gradio*/
        t[16].autoscroll
      )
    },
    { i18n: (
      /*gradio*/
      t[16].i18n
    ) },
    /*loading_status*/
    t[15]
  ];
  let u = {};
  for (let s = 0; s < f.length; s += 1)
    u = Oo(u, f[s]);
  l = new ws({ props: u });
  let o = (
    /*visible*/
    t[6] && Zt(t)
  );
  return {
    c() {
      gl(l.$$.fragment), e = he(), o && o.c(), n = mn();
    },
    m(s, r) {
      pl(l, s, r), K(s, e, r), o && o.m(s, r), K(s, n, r), i = !0;
    },
    p(s, r) {
      const a = r[0] & /*gradio, loading_status*/
      98304 ? Bo(f, [
        r[0] & /*gradio*/
        65536 && {
          autoscroll: (
            /*gradio*/
            s[16].autoscroll
          )
        },
        r[0] & /*gradio*/
        65536 && { i18n: (
          /*gradio*/
          s[16].i18n
        ) },
        r[0] & /*loading_status*/
        32768 && Do(
          /*loading_status*/
          s[15]
        )
      ]) : {};
      l.$set(a), /*visible*/
      s[6] ? o ? (o.p(s, r), r[0] & /*visible*/
      64 && de(o, 1)) : (o = Zt(s), o.c(), de(o, 1), o.m(n.parentNode, n)) : o && (bn(), Se(o, 1, 1, () => {
        o = null;
      }), dn());
    },
    i(s) {
      i || (de(l.$$.fragment, s), de(o), i = !0);
    },
    o(s) {
      Se(l.$$.fragment, s), Se(o), i = !1;
    },
    d(s) {
      s && (G(e), G(n)), wl(l, s), o && o.d(s);
    }
  };
}
function Ro(t) {
  let l, e;
  return l = new On({
    props: {
      visible: (
        /*visible*/
        t[6]
      ),
      elem_id: (
        /*elem_id*/
        t[4]
      ),
      elem_classes: (
        /*elem_classes*/
        t[5]
      ),
      padding: (
        /*container*/
        t[12]
      ),
      allow_overflow: !1,
      scale: (
        /*scale*/
        t[13]
      ),
      min_width: (
        /*min_width*/
        t[14]
      ),
      $$slots: { default: [Jo] },
      $$scope: { ctx: t }
    }
  }), {
    c() {
      gl(l.$$.fragment);
    },
    m(n, i) {
      pl(l, n, i), e = !0;
    },
    p(n, i) {
      const f = {};
      i[0] & /*visible*/
      64 && (f.visible = /*visible*/
      n[6]), i[0] & /*elem_id*/
      16 && (f.elem_id = /*elem_id*/
      n[4]), i[0] & /*elem_classes*/
      32 && (f.elem_classes = /*elem_classes*/
      n[5]), i[0] & /*container*/
      4096 && (f.padding = /*container*/
      n[12]), i[0] & /*scale*/
      8192 && (f.scale = /*scale*/
      n[13]), i[0] & /*min_width*/
      16384 && (f.min_width = /*min_width*/
      n[14]), i[0] & /*elem_id, elem_classes, scale, min_width, show_config, gradio, value, paramsViewNeedUpdate, enable_edition, pipelines, info, show_label, container, default_pipeline, interactive, value_is_output, show_token_textbox, visible, loading_status*/
      524287 | i[1] & /*$$scope*/
      8 && (f.$$scope = { dirty: i, ctx: n }), l.$set(f);
    },
    i(n) {
      e || (de(l.$$.fragment, n), e = !0);
    },
    o(n) {
      Se(l.$$.fragment, n), e = !1;
    },
    d(n) {
      wl(l, n);
    }
  };
}
function Tl(t, l) {
  const e = document.createElement("label");
  e.textContent = l, t.appendChild(e);
}
function Xo(t, l, e) {
  const n = document.createElement("input"), i = t.id;
  Tl(t, i.split("-").at(-1)), n.type = "number", n.value = l, n.contentEditable = String(e), t.appendChild(n);
}
function Yo(t, l, e) {
  let { info: n = void 0 } = l, { elem_id: i = "" } = l, { elem_classes: f = [] } = l, { visible: u = !0 } = l, { value: o = new uo({ name: "", token: "" }) } = l, { value_is_output: s = !1 } = l, { pipelines: r } = l, { default_pipeline: a } = l, { show_label: m } = l, { show_token_textbox: p } = l, { show_config: g = !1 } = l, { enable_edition: j = !1 } = l, { container: k = !0 } = l, { scale: d = null } = l, { min_width: _ = void 0 } = l, { loading_status: w } = l, { gradio: c } = l, { interactive: h } = l, q = !1;
  function v(y) {
    y !== "" && (e(0, o.name = y, o), e(0, o.param_specs = {}, o), c.dispatch("select", o), e(18, q = !0));
  }
  function E(y, Y) {
    const S = y.split("-");
    let V = Ol(o.param_specs);
    var I = V;
    S.forEach((A) => {
      I = I.get(A);
    }), I.set("value", Y), e(0, o.param_specs = cn(V), o);
  }
  function C(y, Y, S) {
    const V = document.createElement("select"), I = y.id;
    Tl(y, I.split("-").at(-1)), Y.forEach((A) => {
      const b = document.createElement("option");
      b.textContent = A, b.value = A, V.appendChild(b), A === S && (b.selected = !0);
    }), V.addEventListener("change", (A) => {
      E(I, V.value);
    }), y.appendChild(V);
  }
  function L(y, Y, S, V, I) {
    const A = document.createElement("input"), b = document.createElement("input"), U = y.id;
    Tl(y, U.split("-").at(-1)), A.type = "range", A.min = Y, A.max = S, A.value = V, A.step = I, A.addEventListener("input", (oe) => {
      b.value = A.value, E(U, A.value);
    }), y.appendChild(A), b.type = "number", b.min = Y, b.max = S, b.value = V, b.step = I, b.contentEditable = "true", b.addEventListener("input", (oe) => {
      A.value = b.value, E(U, A.value);
    }), y.appendChild(b);
  }
  function T(y, Y, S) {
    Y.forEach((V, I) => {
      const A = (S ? S + "-" : "") + I;
      if (V.values().next().value instanceof Map) {
        const b = document.createElement("fieldset");
        b.innerHTML = "<legend>" + A + "<legend>", b.id = A, y.appendChild(b), T(b, V, I);
      } else {
        const b = document.createElement("div");
        switch (b.id = A, b.classList.add("param"), y.appendChild(b), V.get("component")) {
          case "slider":
            L(b, V.get("min"), V.get("max"), V.get("value"), V.get("step"));
            break;
          case "dropdown":
            C(b, V.get("choices"), V.get("value"));
            break;
          case "textbox":
            Xo(b, V.get("value"), !1);
            break;
        }
      }
    });
  }
  Io(() => {
    a && setTimeout(() => v(a), 10);
  });
  function P() {
    o.token = this.value, e(0, o);
  }
  function le(y) {
    s = y, e(2, s);
  }
  const N = () => c.dispatch("input"), J = (y) => v(y.detail.value), R = () => c.dispatch("blur"), me = () => c.dispatch("focus"), ke = (y) => c.dispatch("key_up", y.detail);
  function ve() {
    g = this.checked, e(1, g);
  }
  const ye = () => {
    e(18, q = !0), e(1, g = !g);
  }, F = () => c.dispatch("change", o);
  return t.$$set = (y) => {
    "info" in y && e(3, n = y.info), "elem_id" in y && e(4, i = y.elem_id), "elem_classes" in y && e(5, f = y.elem_classes), "visible" in y && e(6, u = y.visible), "value" in y && e(0, o = y.value), "value_is_output" in y && e(2, s = y.value_is_output), "pipelines" in y && e(7, r = y.pipelines), "default_pipeline" in y && e(8, a = y.default_pipeline), "show_label" in y && e(9, m = y.show_label), "show_token_textbox" in y && e(10, p = y.show_token_textbox), "show_config" in y && e(1, g = y.show_config), "enable_edition" in y && e(11, j = y.enable_edition), "container" in y && e(12, k = y.container), "scale" in y && e(13, d = y.scale), "min_width" in y && e(14, _ = y.min_width), "loading_status" in y && e(15, w = y.loading_status), "gradio" in y && e(16, c = y.gradio), "interactive" in y && e(17, h = y.interactive);
  }, t.$$.update = () => {
    if (t.$$.dirty[0] & /*value, paramsViewNeedUpdate, show_config*/
    262147 && Object.keys(o.param_specs).length > 0 && q) {
      const y = document.getElementById("params-control");
      if (y.replaceChildren(), g) {
        let Y = Ol(o.param_specs);
        T(y, Y), e(18, q = !1);
      }
    }
  }, [
    o,
    g,
    s,
    n,
    i,
    f,
    u,
    r,
    a,
    m,
    p,
    j,
    k,
    d,
    _,
    w,
    c,
    h,
    q,
    v,
    P,
    le,
    N,
    J,
    R,
    me,
    ke,
    ve,
    ye,
    F
  ];
}
class Qo extends Mo {
  constructor(l) {
    super(), To(
      this,
      l,
      Yo,
      Ro,
      Zo,
      {
        info: 3,
        elem_id: 4,
        elem_classes: 5,
        visible: 6,
        value: 0,
        value_is_output: 2,
        pipelines: 7,
        default_pipeline: 8,
        show_label: 9,
        show_token_textbox: 10,
        show_config: 1,
        enable_edition: 11,
        container: 12,
        scale: 13,
        min_width: 14,
        loading_status: 15,
        gradio: 16,
        interactive: 17
      },
      null,
      [-1, -1]
    );
  }
}
export {
  fo as BaseDropdown,
  Go as BaseExample,
  Ko as BaseMultiselect,
  Qo as default
};
