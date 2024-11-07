const {
  SvelteComponent: Oi,
  assign: Pi,
  create_slot: Ui,
  detach: Mi,
  element: Ti,
  get_all_dirty_from_scope: Vi,
  get_slot_changes: Ri,
  get_spread_update: Wi,
  init: Ji,
  insert: Gi,
  safe_not_equal: Zi,
  set_dynamic_element_data: Wn,
  set_style: ue,
  toggle_class: Ce,
  transition_in: ti,
  transition_out: ni,
  update_slot_base: Hi
} = window.__gradio__svelte__internal;
function Ki(n) {
  let e, t, l;
  const i = (
    /*#slots*/
    n[18].default
  ), o = Ui(
    i,
    n,
    /*$$scope*/
    n[17],
    null
  );
  let s = [
    { "data-testid": (
      /*test_id*/
      n[7]
    ) },
    { id: (
      /*elem_id*/
      n[2]
    ) },
    {
      class: t = "block " + /*elem_classes*/
      n[3].join(" ") + " svelte-nl1om8"
    }
  ], f = {};
  for (let a = 0; a < s.length; a += 1)
    f = Pi(f, s[a]);
  return {
    c() {
      e = Ti(
        /*tag*/
        n[14]
      ), o && o.c(), Wn(
        /*tag*/
        n[14]
      )(e, f), Ce(
        e,
        "hidden",
        /*visible*/
        n[10] === !1
      ), Ce(
        e,
        "padded",
        /*padding*/
        n[6]
      ), Ce(
        e,
        "border_focus",
        /*border_mode*/
        n[5] === "focus"
      ), Ce(
        e,
        "border_contrast",
        /*border_mode*/
        n[5] === "contrast"
      ), Ce(e, "hide-container", !/*explicit_call*/
      n[8] && !/*container*/
      n[9]), ue(
        e,
        "height",
        /*get_dimension*/
        n[15](
          /*height*/
          n[0]
        )
      ), ue(e, "width", typeof /*width*/
      n[1] == "number" ? `calc(min(${/*width*/
      n[1]}px, 100%))` : (
        /*get_dimension*/
        n[15](
          /*width*/
          n[1]
        )
      )), ue(
        e,
        "border-style",
        /*variant*/
        n[4]
      ), ue(
        e,
        "overflow",
        /*allow_overflow*/
        n[11] ? "visible" : "hidden"
      ), ue(
        e,
        "flex-grow",
        /*scale*/
        n[12]
      ), ue(e, "min-width", `calc(min(${/*min_width*/
      n[13]}px, 100%))`), ue(e, "border-width", "var(--block-border-width)");
    },
    m(a, r) {
      Gi(a, e, r), o && o.m(e, null), l = !0;
    },
    p(a, r) {
      o && o.p && (!l || r & /*$$scope*/
      131072) && Hi(
        o,
        i,
        a,
        /*$$scope*/
        a[17],
        l ? Ri(
          i,
          /*$$scope*/
          a[17],
          r,
          null
        ) : Vi(
          /*$$scope*/
          a[17]
        ),
        null
      ), Wn(
        /*tag*/
        a[14]
      )(e, f = Wi(s, [
        (!l || r & /*test_id*/
        128) && { "data-testid": (
          /*test_id*/
          a[7]
        ) },
        (!l || r & /*elem_id*/
        4) && { id: (
          /*elem_id*/
          a[2]
        ) },
        (!l || r & /*elem_classes*/
        8 && t !== (t = "block " + /*elem_classes*/
        a[3].join(" ") + " svelte-nl1om8")) && { class: t }
      ])), Ce(
        e,
        "hidden",
        /*visible*/
        a[10] === !1
      ), Ce(
        e,
        "padded",
        /*padding*/
        a[6]
      ), Ce(
        e,
        "border_focus",
        /*border_mode*/
        a[5] === "focus"
      ), Ce(
        e,
        "border_contrast",
        /*border_mode*/
        a[5] === "contrast"
      ), Ce(e, "hide-container", !/*explicit_call*/
      a[8] && !/*container*/
      a[9]), r & /*height*/
      1 && ue(
        e,
        "height",
        /*get_dimension*/
        a[15](
          /*height*/
          a[0]
        )
      ), r & /*width*/
      2 && ue(e, "width", typeof /*width*/
      a[1] == "number" ? `calc(min(${/*width*/
      a[1]}px, 100%))` : (
        /*get_dimension*/
        a[15](
          /*width*/
          a[1]
        )
      )), r & /*variant*/
      16 && ue(
        e,
        "border-style",
        /*variant*/
        a[4]
      ), r & /*allow_overflow*/
      2048 && ue(
        e,
        "overflow",
        /*allow_overflow*/
        a[11] ? "visible" : "hidden"
      ), r & /*scale*/
      4096 && ue(
        e,
        "flex-grow",
        /*scale*/
        a[12]
      ), r & /*min_width*/
      8192 && ue(e, "min-width", `calc(min(${/*min_width*/
      a[13]}px, 100%))`);
    },
    i(a) {
      l || (ti(o, a), l = !0);
    },
    o(a) {
      ni(o, a), l = !1;
    },
    d(a) {
      a && Mi(e), o && o.d(a);
    }
  };
}
function Xi(n) {
  let e, t = (
    /*tag*/
    n[14] && Ki(n)
  );
  return {
    c() {
      t && t.c();
    },
    m(l, i) {
      t && t.m(l, i), e = !0;
    },
    p(l, [i]) {
      /*tag*/
      l[14] && t.p(l, i);
    },
    i(l) {
      e || (ti(t, l), e = !0);
    },
    o(l) {
      ni(t, l), e = !1;
    },
    d(l) {
      t && t.d(l);
    }
  };
}
function Yi(n, e, t) {
  let { $$slots: l = {}, $$scope: i } = e, { height: o = void 0 } = e, { width: s = void 0 } = e, { elem_id: f = "" } = e, { elem_classes: a = [] } = e, { variant: r = "solid" } = e, { border_mode: u = "base" } = e, { padding: c = !0 } = e, { type: d = "normal" } = e, { test_id: _ = void 0 } = e, { explicit_call: m = !1 } = e, { container: y = !0 } = e, { visible: q = !0 } = e, { allow_overflow: w = !0 } = e, { scale: p = null } = e, { min_width: h = 0 } = e, z = d === "fieldset" ? "fieldset" : "div";
  const F = (g) => {
    if (g !== void 0) {
      if (typeof g == "number")
        return g + "px";
      if (typeof g == "string")
        return g;
    }
  };
  return n.$$set = (g) => {
    "height" in g && t(0, o = g.height), "width" in g && t(1, s = g.width), "elem_id" in g && t(2, f = g.elem_id), "elem_classes" in g && t(3, a = g.elem_classes), "variant" in g && t(4, r = g.variant), "border_mode" in g && t(5, u = g.border_mode), "padding" in g && t(6, c = g.padding), "type" in g && t(16, d = g.type), "test_id" in g && t(7, _ = g.test_id), "explicit_call" in g && t(8, m = g.explicit_call), "container" in g && t(9, y = g.container), "visible" in g && t(10, q = g.visible), "allow_overflow" in g && t(11, w = g.allow_overflow), "scale" in g && t(12, p = g.scale), "min_width" in g && t(13, h = g.min_width), "$$scope" in g && t(17, i = g.$$scope);
  }, [
    o,
    s,
    f,
    a,
    r,
    u,
    c,
    _,
    m,
    y,
    q,
    w,
    p,
    h,
    z,
    F,
    d,
    i,
    l
  ];
}
class Qi extends Oi {
  constructor(e) {
    super(), Ji(this, e, Yi, Xi, Zi, {
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
  SvelteComponent: xi,
  append: ln,
  attr: Et,
  create_component: $i,
  destroy_component: eo,
  detach: to,
  element: Jn,
  init: no,
  insert: lo,
  mount_component: io,
  safe_not_equal: oo,
  set_data: so,
  space: ao,
  text: ro,
  toggle_class: Ue,
  transition_in: fo,
  transition_out: uo
} = window.__gradio__svelte__internal;
function co(n) {
  let e, t, l, i, o, s;
  return l = new /*Icon*/
  n[1]({}), {
    c() {
      e = Jn("label"), t = Jn("span"), $i(l.$$.fragment), i = ao(), o = ro(
        /*label*/
        n[0]
      ), Et(t, "class", "svelte-9gxdi0"), Et(e, "for", ""), Et(e, "data-testid", "block-label"), Et(e, "class", "svelte-9gxdi0"), Ue(e, "hide", !/*show_label*/
      n[2]), Ue(e, "sr-only", !/*show_label*/
      n[2]), Ue(
        e,
        "float",
        /*float*/
        n[4]
      ), Ue(
        e,
        "hide-label",
        /*disable*/
        n[3]
      );
    },
    m(f, a) {
      lo(f, e, a), ln(e, t), io(l, t, null), ln(e, i), ln(e, o), s = !0;
    },
    p(f, [a]) {
      (!s || a & /*label*/
      1) && so(
        o,
        /*label*/
        f[0]
      ), (!s || a & /*show_label*/
      4) && Ue(e, "hide", !/*show_label*/
      f[2]), (!s || a & /*show_label*/
      4) && Ue(e, "sr-only", !/*show_label*/
      f[2]), (!s || a & /*float*/
      16) && Ue(
        e,
        "float",
        /*float*/
        f[4]
      ), (!s || a & /*disable*/
      8) && Ue(
        e,
        "hide-label",
        /*disable*/
        f[3]
      );
    },
    i(f) {
      s || (fo(l.$$.fragment, f), s = !0);
    },
    o(f) {
      uo(l.$$.fragment, f), s = !1;
    },
    d(f) {
      f && to(e), eo(l);
    }
  };
}
function _o(n, e, t) {
  let { label: l = null } = e, { Icon: i } = e, { show_label: o = !0 } = e, { disable: s = !1 } = e, { float: f = !0 } = e;
  return n.$$set = (a) => {
    "label" in a && t(0, l = a.label), "Icon" in a && t(1, i = a.Icon), "show_label" in a && t(2, o = a.show_label), "disable" in a && t(3, s = a.disable), "float" in a && t(4, f = a.float);
  }, [l, i, o, s, f];
}
class li extends xi {
  constructor(e) {
    super(), no(this, e, _o, co, oo, {
      label: 0,
      Icon: 1,
      show_label: 2,
      disable: 3,
      float: 4
    });
  }
}
const {
  SvelteComponent: mo,
  append: yn,
  attr: Ae,
  bubble: go,
  create_component: ho,
  destroy_component: po,
  detach: ii,
  element: qn,
  init: bo,
  insert: oi,
  listen: wo,
  mount_component: vo,
  safe_not_equal: ko,
  set_data: yo,
  set_style: at,
  space: qo,
  text: So,
  toggle_class: re,
  transition_in: Co,
  transition_out: zo
} = window.__gradio__svelte__internal;
function Gn(n) {
  let e, t;
  return {
    c() {
      e = qn("span"), t = So(
        /*label*/
        n[1]
      ), Ae(e, "class", "svelte-1lrphxw");
    },
    m(l, i) {
      oi(l, e, i), yn(e, t);
    },
    p(l, i) {
      i & /*label*/
      2 && yo(
        t,
        /*label*/
        l[1]
      );
    },
    d(l) {
      l && ii(e);
    }
  };
}
function Do(n) {
  let e, t, l, i, o, s, f, a = (
    /*show_label*/
    n[2] && Gn(n)
  );
  return i = new /*Icon*/
  n[0]({}), {
    c() {
      e = qn("button"), a && a.c(), t = qo(), l = qn("div"), ho(i.$$.fragment), Ae(l, "class", "svelte-1lrphxw"), re(
        l,
        "small",
        /*size*/
        n[4] === "small"
      ), re(
        l,
        "large",
        /*size*/
        n[4] === "large"
      ), re(
        l,
        "medium",
        /*size*/
        n[4] === "medium"
      ), e.disabled = /*disabled*/
      n[7], Ae(
        e,
        "aria-label",
        /*label*/
        n[1]
      ), Ae(
        e,
        "aria-haspopup",
        /*hasPopup*/
        n[8]
      ), Ae(
        e,
        "title",
        /*label*/
        n[1]
      ), Ae(e, "class", "svelte-1lrphxw"), re(
        e,
        "pending",
        /*pending*/
        n[3]
      ), re(
        e,
        "padded",
        /*padded*/
        n[5]
      ), re(
        e,
        "highlight",
        /*highlight*/
        n[6]
      ), re(
        e,
        "transparent",
        /*transparent*/
        n[9]
      ), at(e, "color", !/*disabled*/
      n[7] && /*_color*/
      n[12] ? (
        /*_color*/
        n[12]
      ) : "var(--block-label-text-color)"), at(e, "--bg-color", /*disabled*/
      n[7] ? "auto" : (
        /*background*/
        n[10]
      )), at(
        e,
        "margin-left",
        /*offset*/
        n[11] + "px"
      );
    },
    m(r, u) {
      oi(r, e, u), a && a.m(e, null), yn(e, t), yn(e, l), vo(i, l, null), o = !0, s || (f = wo(
        e,
        "click",
        /*click_handler*/
        n[14]
      ), s = !0);
    },
    p(r, [u]) {
      /*show_label*/
      r[2] ? a ? a.p(r, u) : (a = Gn(r), a.c(), a.m(e, t)) : a && (a.d(1), a = null), (!o || u & /*size*/
      16) && re(
        l,
        "small",
        /*size*/
        r[4] === "small"
      ), (!o || u & /*size*/
      16) && re(
        l,
        "large",
        /*size*/
        r[4] === "large"
      ), (!o || u & /*size*/
      16) && re(
        l,
        "medium",
        /*size*/
        r[4] === "medium"
      ), (!o || u & /*disabled*/
      128) && (e.disabled = /*disabled*/
      r[7]), (!o || u & /*label*/
      2) && Ae(
        e,
        "aria-label",
        /*label*/
        r[1]
      ), (!o || u & /*hasPopup*/
      256) && Ae(
        e,
        "aria-haspopup",
        /*hasPopup*/
        r[8]
      ), (!o || u & /*label*/
      2) && Ae(
        e,
        "title",
        /*label*/
        r[1]
      ), (!o || u & /*pending*/
      8) && re(
        e,
        "pending",
        /*pending*/
        r[3]
      ), (!o || u & /*padded*/
      32) && re(
        e,
        "padded",
        /*padded*/
        r[5]
      ), (!o || u & /*highlight*/
      64) && re(
        e,
        "highlight",
        /*highlight*/
        r[6]
      ), (!o || u & /*transparent*/
      512) && re(
        e,
        "transparent",
        /*transparent*/
        r[9]
      ), u & /*disabled, _color*/
      4224 && at(e, "color", !/*disabled*/
      r[7] && /*_color*/
      r[12] ? (
        /*_color*/
        r[12]
      ) : "var(--block-label-text-color)"), u & /*disabled, background*/
      1152 && at(e, "--bg-color", /*disabled*/
      r[7] ? "auto" : (
        /*background*/
        r[10]
      )), u & /*offset*/
      2048 && at(
        e,
        "margin-left",
        /*offset*/
        r[11] + "px"
      );
    },
    i(r) {
      o || (Co(i.$$.fragment, r), o = !0);
    },
    o(r) {
      zo(i.$$.fragment, r), o = !1;
    },
    d(r) {
      r && ii(e), a && a.d(), po(i), s = !1, f();
    }
  };
}
function Eo(n, e, t) {
  let l, { Icon: i } = e, { label: o = "" } = e, { show_label: s = !1 } = e, { pending: f = !1 } = e, { size: a = "small" } = e, { padded: r = !0 } = e, { highlight: u = !1 } = e, { disabled: c = !1 } = e, { hasPopup: d = !1 } = e, { color: _ = "var(--block-label-text-color)" } = e, { transparent: m = !1 } = e, { background: y = "var(--background-fill-primary)" } = e, { offset: q = 0 } = e;
  function w(p) {
    go.call(this, n, p);
  }
  return n.$$set = (p) => {
    "Icon" in p && t(0, i = p.Icon), "label" in p && t(1, o = p.label), "show_label" in p && t(2, s = p.show_label), "pending" in p && t(3, f = p.pending), "size" in p && t(4, a = p.size), "padded" in p && t(5, r = p.padded), "highlight" in p && t(6, u = p.highlight), "disabled" in p && t(7, c = p.disabled), "hasPopup" in p && t(8, d = p.hasPopup), "color" in p && t(13, _ = p.color), "transparent" in p && t(9, m = p.transparent), "background" in p && t(10, y = p.background), "offset" in p && t(11, q = p.offset);
  }, n.$$.update = () => {
    n.$$.dirty & /*highlight, color*/
    8256 && t(12, l = u ? "var(--color-accent)" : _);
  }, [
    i,
    o,
    s,
    f,
    a,
    r,
    u,
    c,
    d,
    m,
    y,
    q,
    l,
    _,
    w
  ];
}
let jo = class extends mo {
  constructor(e) {
    super(), bo(this, e, Eo, Do, ko, {
      Icon: 0,
      label: 1,
      show_label: 2,
      pending: 3,
      size: 4,
      padded: 5,
      highlight: 6,
      disabled: 7,
      hasPopup: 8,
      color: 13,
      transparent: 9,
      background: 10,
      offset: 11
    });
  }
};
const {
  SvelteComponent: No,
  append: Fo,
  attr: on,
  binding_callbacks: Ao,
  create_slot: Lo,
  detach: Bo,
  element: Zn,
  get_all_dirty_from_scope: Io,
  get_slot_changes: Oo,
  init: Po,
  insert: Uo,
  safe_not_equal: Mo,
  toggle_class: Me,
  transition_in: To,
  transition_out: Vo,
  update_slot_base: Ro
} = window.__gradio__svelte__internal;
function Wo(n) {
  let e, t, l;
  const i = (
    /*#slots*/
    n[5].default
  ), o = Lo(
    i,
    n,
    /*$$scope*/
    n[4],
    null
  );
  return {
    c() {
      e = Zn("div"), t = Zn("div"), o && o.c(), on(t, "class", "icon svelte-3w3rth"), on(e, "class", "empty svelte-3w3rth"), on(e, "aria-label", "Empty value"), Me(
        e,
        "small",
        /*size*/
        n[0] === "small"
      ), Me(
        e,
        "large",
        /*size*/
        n[0] === "large"
      ), Me(
        e,
        "unpadded_box",
        /*unpadded_box*/
        n[1]
      ), Me(
        e,
        "small_parent",
        /*parent_height*/
        n[3]
      );
    },
    m(s, f) {
      Uo(s, e, f), Fo(e, t), o && o.m(t, null), n[6](e), l = !0;
    },
    p(s, [f]) {
      o && o.p && (!l || f & /*$$scope*/
      16) && Ro(
        o,
        i,
        s,
        /*$$scope*/
        s[4],
        l ? Oo(
          i,
          /*$$scope*/
          s[4],
          f,
          null
        ) : Io(
          /*$$scope*/
          s[4]
        ),
        null
      ), (!l || f & /*size*/
      1) && Me(
        e,
        "small",
        /*size*/
        s[0] === "small"
      ), (!l || f & /*size*/
      1) && Me(
        e,
        "large",
        /*size*/
        s[0] === "large"
      ), (!l || f & /*unpadded_box*/
      2) && Me(
        e,
        "unpadded_box",
        /*unpadded_box*/
        s[1]
      ), (!l || f & /*parent_height*/
      8) && Me(
        e,
        "small_parent",
        /*parent_height*/
        s[3]
      );
    },
    i(s) {
      l || (To(o, s), l = !0);
    },
    o(s) {
      Vo(o, s), l = !1;
    },
    d(s) {
      s && Bo(e), o && o.d(s), n[6](null);
    }
  };
}
function Jo(n, e, t) {
  let l, { $$slots: i = {}, $$scope: o } = e, { size: s = "small" } = e, { unpadded_box: f = !1 } = e, a;
  function r(c) {
    var d;
    if (!c) return !1;
    const { height: _ } = c.getBoundingClientRect(), { height: m } = ((d = c.parentElement) === null || d === void 0 ? void 0 : d.getBoundingClientRect()) || { height: _ };
    return _ > m + 2;
  }
  function u(c) {
    Ao[c ? "unshift" : "push"](() => {
      a = c, t(2, a);
    });
  }
  return n.$$set = (c) => {
    "size" in c && t(0, s = c.size), "unpadded_box" in c && t(1, f = c.unpadded_box), "$$scope" in c && t(4, o = c.$$scope);
  }, n.$$.update = () => {
    n.$$.dirty & /*el*/
    4 && t(3, l = r(a));
  }, [s, f, a, l, o, i, u];
}
class Go extends No {
  constructor(e) {
    super(), Po(this, e, Jo, Wo, Mo, { size: 0, unpadded_box: 1 });
  }
}
const {
  SvelteComponent: Zo,
  append: Ho,
  attr: jt,
  detach: Ko,
  init: Xo,
  insert: Yo,
  noop: sn,
  safe_not_equal: Qo,
  svg_element: Hn
} = window.__gradio__svelte__internal;
function xo(n) {
  let e, t;
  return {
    c() {
      e = Hn("svg"), t = Hn("path"), jt(t, "fill", "currentColor"), jt(t, "d", "M13.75 2a2.25 2.25 0 0 1 2.236 2.002V4h1.764A2.25 2.25 0 0 1 20 6.25V11h-1.5V6.25a.75.75 0 0 0-.75-.75h-2.129c-.404.603-1.091 1-1.871 1h-3.5c-.78 0-1.467-.397-1.871-1H6.25a.75.75 0 0 0-.75.75v13.5c0 .414.336.75.75.75h4.78a4 4 0 0 0 .505 1.5H6.25A2.25 2.25 0 0 1 4 19.75V6.25A2.25 2.25 0 0 1 6.25 4h1.764a2.25 2.25 0 0 1 2.236-2zm2.245 2.096L16 4.25q0-.078-.005-.154M13.75 3.5h-3.5a.75.75 0 0 0 0 1.5h3.5a.75.75 0 0 0 0-1.5M15 12a3 3 0 0 0-3 3v5c0 .556.151 1.077.415 1.524l3.494-3.494a2.25 2.25 0 0 1 3.182 0l3.494 3.494c.264-.447.415-.968.415-1.524v-5a3 3 0 0 0-3-3zm0 11a3 3 0 0 1-1.524-.415l3.494-3.494a.75.75 0 0 1 1.06 0l3.494 3.494A3 3 0 0 1 20 23zm5-7a1 1 0 1 1 0-2 1 1 0 0 1 0 2"), jt(e, "xmlns", "http://www.w3.org/2000/svg"), jt(e, "viewBox", "0 0 24 24");
    },
    m(l, i) {
      Yo(l, e, i), Ho(e, t);
    },
    p: sn,
    i: sn,
    o: sn,
    d(l) {
      l && Ko(e);
    }
  };
}
class $o extends Zo {
  constructor(e) {
    super(), Xo(this, e, null, xo, Qo, {});
  }
}
const {
  SvelteComponent: es,
  append: an,
  attr: ie,
  detach: ts,
  init: ns,
  insert: ls,
  noop: rn,
  safe_not_equal: is,
  svg_element: Nt
} = window.__gradio__svelte__internal;
function os(n) {
  let e, t, l, i;
  return {
    c() {
      e = Nt("svg"), t = Nt("path"), l = Nt("polyline"), i = Nt("line"), ie(t, "d", "M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"), ie(l, "points", "17 8 12 3 7 8"), ie(i, "x1", "12"), ie(i, "y1", "3"), ie(i, "x2", "12"), ie(i, "y2", "15"), ie(e, "xmlns", "http://www.w3.org/2000/svg"), ie(e, "width", "90%"), ie(e, "height", "90%"), ie(e, "viewBox", "0 0 24 24"), ie(e, "fill", "none"), ie(e, "stroke", "currentColor"), ie(e, "stroke-width", "2"), ie(e, "stroke-linecap", "round"), ie(e, "stroke-linejoin", "round"), ie(e, "class", "feather feather-upload");
    },
    m(o, s) {
      ls(o, e, s), an(e, t), an(e, l), an(e, i);
    },
    p: rn,
    i: rn,
    o: rn,
    d(o) {
      o && ts(e);
    }
  };
}
let ss = class extends es {
  constructor(e) {
    super(), ns(this, e, null, os, is, {});
  }
};
const as = [
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
], Kn = {
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
as.reduce(
  (n, { color: e, primary: t, secondary: l }) => ({
    ...n,
    [e]: {
      primary: Kn[e][t],
      secondary: Kn[e][l]
    }
  }),
  {}
);
const {
  SvelteComponent: rs,
  append: Xe,
  attr: Sn,
  check_outros: fs,
  create_component: si,
  destroy_component: ai,
  detach: Pt,
  element: Cn,
  group_outros: us,
  init: cs,
  insert: Ut,
  mount_component: ri,
  safe_not_equal: _s,
  set_data: zn,
  space: Dn,
  text: kt,
  toggle_class: Xn,
  transition_in: Tt,
  transition_out: Vt
} = window.__gradio__svelte__internal;
function ds(n) {
  let e, t;
  return e = new ss({}), {
    c() {
      si(e.$$.fragment);
    },
    m(l, i) {
      ri(e, l, i), t = !0;
    },
    i(l) {
      t || (Tt(e.$$.fragment, l), t = !0);
    },
    o(l) {
      Vt(e.$$.fragment, l), t = !1;
    },
    d(l) {
      ai(e, l);
    }
  };
}
function ms(n) {
  let e, t;
  return e = new $o({}), {
    c() {
      si(e.$$.fragment);
    },
    m(l, i) {
      ri(e, l, i), t = !0;
    },
    i(l) {
      t || (Tt(e.$$.fragment, l), t = !0);
    },
    o(l) {
      Vt(e.$$.fragment, l), t = !1;
    },
    d(l) {
      ai(e, l);
    }
  };
}
function Yn(n) {
  let e, t, l = (
    /*i18n*/
    n[1]("common.or") + ""
  ), i, o, s, f = (
    /*message*/
    (n[2] || /*i18n*/
    n[1]("upload_text.click_to_upload")) + ""
  ), a;
  return {
    c() {
      e = Cn("span"), t = kt("- "), i = kt(l), o = kt(" -"), s = Dn(), a = kt(f), Sn(e, "class", "or svelte-kzcjhc");
    },
    m(r, u) {
      Ut(r, e, u), Xe(e, t), Xe(e, i), Xe(e, o), Ut(r, s, u), Ut(r, a, u);
    },
    p(r, u) {
      u & /*i18n*/
      2 && l !== (l = /*i18n*/
      r[1]("common.or") + "") && zn(i, l), u & /*message, i18n*/
      6 && f !== (f = /*message*/
      (r[2] || /*i18n*/
      r[1]("upload_text.click_to_upload")) + "") && zn(a, f);
    },
    d(r) {
      r && (Pt(e), Pt(s), Pt(a));
    }
  };
}
function gs(n) {
  let e, t, l, i, o, s = (
    /*i18n*/
    n[1](
      /*defs*/
      n[5][
        /*type*/
        n[0]
      ] || /*defs*/
      n[5].file
    ) + ""
  ), f, a, r;
  const u = [ms, ds], c = [];
  function d(m, y) {
    return (
      /*type*/
      m[0] === "clipboard" ? 0 : 1
    );
  }
  l = d(n), i = c[l] = u[l](n);
  let _ = (
    /*mode*/
    n[3] !== "short" && Yn(n)
  );
  return {
    c() {
      e = Cn("div"), t = Cn("span"), i.c(), o = Dn(), f = kt(s), a = Dn(), _ && _.c(), Sn(t, "class", "icon-wrap svelte-kzcjhc"), Xn(
        t,
        "hovered",
        /*hovered*/
        n[4]
      ), Sn(e, "class", "wrap svelte-kzcjhc");
    },
    m(m, y) {
      Ut(m, e, y), Xe(e, t), c[l].m(t, null), Xe(e, o), Xe(e, f), Xe(e, a), _ && _.m(e, null), r = !0;
    },
    p(m, [y]) {
      let q = l;
      l = d(m), l !== q && (us(), Vt(c[q], 1, 1, () => {
        c[q] = null;
      }), fs(), i = c[l], i || (i = c[l] = u[l](m), i.c()), Tt(i, 1), i.m(t, null)), (!r || y & /*hovered*/
      16) && Xn(
        t,
        "hovered",
        /*hovered*/
        m[4]
      ), (!r || y & /*i18n, type*/
      3) && s !== (s = /*i18n*/
      m[1](
        /*defs*/
        m[5][
          /*type*/
          m[0]
        ] || /*defs*/
        m[5].file
      ) + "") && zn(f, s), /*mode*/
      m[3] !== "short" ? _ ? _.p(m, y) : (_ = Yn(m), _.c(), _.m(e, null)) : _ && (_.d(1), _ = null);
    },
    i(m) {
      r || (Tt(i), r = !0);
    },
    o(m) {
      Vt(i), r = !1;
    },
    d(m) {
      m && Pt(e), c[l].d(), _ && _.d();
    }
  };
}
function hs(n, e, t) {
  let { type: l = "file" } = e, { i18n: i } = e, { message: o = void 0 } = e, { mode: s = "full" } = e, { hovered: f = !1 } = e;
  const a = {
    image: "upload_text.drop_image",
    video: "upload_text.drop_video",
    audio: "upload_text.drop_audio",
    file: "upload_text.drop_file",
    csv: "upload_text.drop_csv",
    gallery: "upload_text.drop_gallery",
    clipboard: "upload_text.paste_clipboard"
  };
  return n.$$set = (r) => {
    "type" in r && t(0, l = r.type), "i18n" in r && t(1, i = r.i18n), "message" in r && t(2, o = r.message), "mode" in r && t(3, s = r.mode), "hovered" in r && t(4, f = r.hovered);
  }, [l, i, o, s, f, a];
}
class ps extends rs {
  constructor(e) {
    super(), cs(this, e, hs, gs, _s, {
      type: 0,
      i18n: 1,
      message: 2,
      mode: 3,
      hovered: 4
    });
  }
}
const {
  SvelteComponent: bs,
  append: fn,
  attr: ke,
  detach: ws,
  init: vs,
  insert: ks,
  noop: un,
  safe_not_equal: ys,
  set_style: ze,
  svg_element: Ft
} = window.__gradio__svelte__internal;
function qs(n) {
  let e, t, l, i;
  return {
    c() {
      e = Ft("svg"), t = Ft("g"), l = Ft("path"), i = Ft("path"), ke(l, "d", "M18,6L6.087,17.913"), ze(l, "fill", "none"), ze(l, "fill-rule", "nonzero"), ze(l, "stroke-width", "2px"), ke(t, "transform", "matrix(1.14096,-0.140958,-0.140958,1.14096,-0.0559523,0.0559523)"), ke(i, "d", "M4.364,4.364L19.636,19.636"), ze(i, "fill", "none"), ze(i, "fill-rule", "nonzero"), ze(i, "stroke-width", "2px"), ke(e, "width", "100%"), ke(e, "height", "100%"), ke(e, "viewBox", "0 0 24 24"), ke(e, "version", "1.1"), ke(e, "xmlns", "http://www.w3.org/2000/svg"), ke(e, "xmlns:xlink", "http://www.w3.org/1999/xlink"), ke(e, "xml:space", "preserve"), ke(e, "stroke", "currentColor"), ze(e, "fill-rule", "evenodd"), ze(e, "clip-rule", "evenodd"), ze(e, "stroke-linecap", "round"), ze(e, "stroke-linejoin", "round");
    },
    m(o, s) {
      ks(o, e, s), fn(e, t), fn(t, l), fn(e, i);
    },
    p: un,
    i: un,
    o: un,
    d(o) {
      o && ws(e);
    }
  };
}
class Ss extends bs {
  constructor(e) {
    super(), vs(this, e, null, qs, ys, {});
  }
}
const {
  SvelteComponent: Cs,
  append: zs,
  attr: rt,
  detach: Ds,
  init: Es,
  insert: js,
  noop: cn,
  safe_not_equal: Ns,
  svg_element: Qn
} = window.__gradio__svelte__internal;
function Fs(n) {
  let e, t;
  return {
    c() {
      e = Qn("svg"), t = Qn("path"), rt(t, "fill", "currentColor"), rt(t, "d", "M26 24v4H6v-4H4v4a2 2 0 0 0 2 2h20a2 2 0 0 0 2-2v-4zm0-10l-1.41-1.41L17 20.17V2h-2v18.17l-7.59-7.58L6 14l10 10l10-10z"), rt(e, "xmlns", "http://www.w3.org/2000/svg"), rt(e, "width", "100%"), rt(e, "height", "100%"), rt(e, "viewBox", "0 0 32 32");
    },
    m(l, i) {
      js(l, e, i), zs(e, t);
    },
    p: cn,
    i: cn,
    o: cn,
    d(l) {
      l && Ds(e);
    }
  };
}
class As extends Cs {
  constructor(e) {
    super(), Es(this, e, null, Fs, Ns, {});
  }
}
const {
  SvelteComponent: Ls,
  append: Bs,
  attr: ye,
  detach: Is,
  init: Os,
  insert: Ps,
  noop: _n,
  safe_not_equal: Us,
  svg_element: xn
} = window.__gradio__svelte__internal;
function Ms(n) {
  let e, t;
  return {
    c() {
      e = xn("svg"), t = xn("path"), ye(t, "d", "M17 3a2.828 2.828 0 1 1 4 4L7.5 20.5 2 22l1.5-5.5L17 3z"), ye(e, "xmlns", "http://www.w3.org/2000/svg"), ye(e, "width", "100%"), ye(e, "height", "100%"), ye(e, "viewBox", "0 0 24 24"), ye(e, "fill", "none"), ye(e, "stroke", "currentColor"), ye(e, "stroke-width", "1.5"), ye(e, "stroke-linecap", "round"), ye(e, "stroke-linejoin", "round"), ye(e, "class", "feather feather-edit-2");
    },
    m(l, i) {
      Ps(l, e, i), Bs(e, t);
    },
    p: _n,
    i: _n,
    o: _n,
    d(l) {
      l && Is(e);
    }
  };
}
class Ts extends Ls {
  constructor(e) {
    super(), Os(this, e, null, Ms, Us, {});
  }
}
const {
  SvelteComponent: Vs,
  append: $n,
  attr: me,
  detach: Rs,
  init: Ws,
  insert: Js,
  noop: dn,
  safe_not_equal: Gs,
  svg_element: mn
} = window.__gradio__svelte__internal;
function Zs(n) {
  let e, t, l;
  return {
    c() {
      e = mn("svg"), t = mn("path"), l = mn("polyline"), me(t, "d", "M13 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V9z"), me(l, "points", "13 2 13 9 20 9"), me(e, "xmlns", "http://www.w3.org/2000/svg"), me(e, "width", "100%"), me(e, "height", "100%"), me(e, "viewBox", "0 0 24 24"), me(e, "fill", "none"), me(e, "stroke", "currentColor"), me(e, "stroke-width", "1.5"), me(e, "stroke-linecap", "round"), me(e, "stroke-linejoin", "round"), me(e, "class", "feather feather-file");
    },
    m(i, o) {
      Js(i, e, o), $n(e, t), $n(e, l);
    },
    p: dn,
    i: dn,
    o: dn,
    d(i) {
      i && Rs(e);
    }
  };
}
let Un = class extends Vs {
  constructor(e) {
    super(), Ws(this, e, null, Zs, Gs, {});
  }
};
const {
  SvelteComponent: Hs,
  append: el,
  attr: ge,
  detach: Ks,
  init: Xs,
  insert: Ys,
  noop: gn,
  safe_not_equal: Qs,
  svg_element: hn
} = window.__gradio__svelte__internal;
function xs(n) {
  let e, t, l;
  return {
    c() {
      e = hn("svg"), t = hn("polyline"), l = hn("path"), ge(t, "points", "1 4 1 10 7 10"), ge(l, "d", "M3.51 15a9 9 0 1 0 2.13-9.36L1 10"), ge(e, "xmlns", "http://www.w3.org/2000/svg"), ge(e, "width", "100%"), ge(e, "height", "100%"), ge(e, "viewBox", "0 0 24 24"), ge(e, "fill", "none"), ge(e, "stroke", "currentColor"), ge(e, "stroke-width", "2"), ge(e, "stroke-linecap", "round"), ge(e, "stroke-linejoin", "round"), ge(e, "class", "feather feather-rotate-ccw");
    },
    m(i, o) {
      Ys(i, e, o), el(e, t), el(e, l);
    },
    p: gn,
    i: gn,
    o: gn,
    d(i) {
      i && Ks(e);
    }
  };
}
class $s extends Hs {
  constructor(e) {
    super(), Xs(this, e, null, xs, Qs, {});
  }
}
const {
  SvelteComponent: ea,
  append: _e,
  attr: ee,
  check_outros: fi,
  create_component: ta,
  destroy_component: na,
  destroy_each: la,
  detach: xe,
  element: be,
  ensure_array_like: tl,
  group_outros: ui,
  init: ia,
  insert: $e,
  listen: oa,
  mount_component: sa,
  noop: nl,
  safe_not_equal: aa,
  set_data: Rt,
  set_style: ll,
  space: At,
  text: Wt,
  toggle_class: il,
  transition_in: dt,
  transition_out: qt
} = window.__gradio__svelte__internal, { createEventDispatcher: ra } = window.__gradio__svelte__internal;
function ol(n, e, t) {
  const l = n.slice();
  return l[7] = e[t], l[9] = t, l;
}
function fa(n) {
  let e = (
    /*i18n*/
    n[2]("file.uploading") + ""
  ), t;
  return {
    c() {
      t = Wt(e);
    },
    m(l, i) {
      $e(l, t, i);
    },
    p(l, i) {
      i & /*i18n*/
      4 && e !== (e = /*i18n*/
      l[2]("file.uploading") + "") && Rt(t, e);
    },
    i: nl,
    o: nl,
    d(l) {
      l && xe(t);
    }
  };
}
function ua(n) {
  let e, t, l, i, o, s;
  return l = new jo({ props: { Icon: As } }), {
    c() {
      e = be("button"), t = be("a"), ta(l.$$.fragment), ee(t, "href", i = /*file*/
      n[7].url), ee(t, "target", "_blank"), ee(t, "download", o = /*file*/
      n[7].orig_name);
    },
    m(f, a) {
      $e(f, e, a), _e(e, t), sa(l, t, null), s = !0;
    },
    p(f, a) {
      (!s || a & /*normalized_files*/
      8 && i !== (i = /*file*/
      f[7].url)) && ee(t, "href", i), (!s || a & /*normalized_files*/
      8 && o !== (o = /*file*/
      f[7].orig_name)) && ee(t, "download", o);
    },
    i(f) {
      s || (dt(l.$$.fragment, f), s = !0);
    },
    o(f) {
      qt(l.$$.fragment, f), s = !1;
    },
    d(f) {
      f && xe(e), na(l);
    }
  };
}
function sl(n) {
  let e = rl(
    /*file*/
    n[7].url,
    "file-content-" + /*i*/
    n[9].toString()
  ) + "", t;
  return {
    c() {
      t = Wt(e);
    },
    m(l, i) {
      $e(l, t, i);
    },
    p(l, i) {
      i & /*normalized_files*/
      8 && e !== (e = rl(
        /*file*/
        l[7].url,
        "file-content-" + /*i*/
        l[9].toString()
      ) + "") && Rt(t, e);
    },
    d(l) {
      l && xe(t);
    }
  };
}
function al(n) {
  let e, t, l, i = (
    /*file*/
    n[7].filename_stem + ""
  ), o, s, f, a = (
    /*file*/
    n[7].filename_ext + ""
  ), r, u, c, d, _, m, y, q, w, p, h, z, F;
  const g = [ua, fa], D = [];
  function T(I, W) {
    return (
      /*file*/
      I[7].url ? 0 : 1
    );
  }
  _ = T(n), m = D[_] = g[_](n);
  function S() {
    return (
      /*click_handler*/
      n[6](
        /*file*/
        n[7],
        /*i*/
        n[9]
      )
    );
  }
  let B = (
    /*file*/
    n[7].url && sl(n)
  );
  return {
    c() {
      e = be("tr"), t = be("td"), l = be("span"), o = Wt(i), s = At(), f = be("span"), r = Wt(a), c = At(), d = be("td"), m.c(), y = At(), q = be("tr"), w = be("td"), B && B.c(), p = At(), ee(l, "class", "stem svelte-a45z3z"), ee(f, "class", "ext svelte-a45z3z"), ee(t, "class", "filename svelte-a45z3z"), ee(t, "aria-label", u = /*file*/
      n[7].orig_name), ee(d, "class", "download svelte-a45z3z"), ee(e, "class", "file svelte-a45z3z"), il(
        e,
        "selectable",
        /*selectable*/
        n[0]
      ), ee(q, "class", "file-content svelte-a45z3z"), ee(q, "id", "file-content-" + /*i*/
      n[9]);
    },
    m(I, W) {
      $e(I, e, W), _e(e, t), _e(t, l), _e(l, o), _e(t, s), _e(t, f), _e(f, r), _e(e, c), _e(e, d), D[_].m(d, null), $e(I, y, W), $e(I, q, W), _e(q, w), B && B.m(w, null), _e(q, p), h = !0, z || (F = oa(e, "click", S), z = !0);
    },
    p(I, W) {
      n = I, (!h || W & /*normalized_files*/
      8) && i !== (i = /*file*/
      n[7].filename_stem + "") && Rt(o, i), (!h || W & /*normalized_files*/
      8) && a !== (a = /*file*/
      n[7].filename_ext + "") && Rt(r, a), (!h || W & /*normalized_files*/
      8 && u !== (u = /*file*/
      n[7].orig_name)) && ee(t, "aria-label", u);
      let G = _;
      _ = T(n), _ === G ? D[_].p(n, W) : (ui(), qt(D[G], 1, 1, () => {
        D[G] = null;
      }), fi(), m = D[_], m ? m.p(n, W) : (m = D[_] = g[_](n), m.c()), dt(m, 1), m.m(d, null)), (!h || W & /*selectable*/
      1) && il(
        e,
        "selectable",
        /*selectable*/
        n[0]
      ), /*file*/
      n[7].url ? B ? B.p(n, W) : (B = sl(n), B.c(), B.m(w, null)) : B && (B.d(1), B = null);
    },
    i(I) {
      h || (dt(m), h = !0);
    },
    o(I) {
      qt(m), h = !1;
    },
    d(I) {
      I && (xe(e), xe(y), xe(q)), D[_].d(), B && B.d(), z = !1, F();
    }
  };
}
function ca(n) {
  let e, t, l, i, o = tl(
    /*normalized_files*/
    n[3]
  ), s = [];
  for (let a = 0; a < o.length; a += 1)
    s[a] = al(ol(n, o, a));
  const f = (a) => qt(s[a], 1, 1, () => {
    s[a] = null;
  });
  return {
    c() {
      e = be("div"), t = be("table"), l = be("tbody");
      for (let a = 0; a < s.length; a += 1)
        s[a].c();
      ee(l, "class", "svelte-a45z3z"), ee(t, "class", "file-preview svelte-a45z3z"), ee(e, "class", "file-preview-holder"), ll(e, "max-height", typeof /*height*/
      n[1] === void 0 ? "auto" : (
        /*height*/
        n[1] + "px"
      ));
    },
    m(a, r) {
      $e(a, e, r), _e(e, t), _e(t, l);
      for (let u = 0; u < s.length; u += 1)
        s[u] && s[u].m(l, null);
      i = !0;
    },
    p(a, [r]) {
      if (r & /*getFileContent, normalized_files, selectable, dispatch, i18n*/
      29) {
        o = tl(
          /*normalized_files*/
          a[3]
        );
        let u;
        for (u = 0; u < o.length; u += 1) {
          const c = ol(a, o, u);
          s[u] ? (s[u].p(c, r), dt(s[u], 1)) : (s[u] = al(c), s[u].c(), dt(s[u], 1), s[u].m(l, null));
        }
        for (ui(), u = o.length; u < s.length; u += 1)
          f(u);
        fi();
      }
      (!i || r & /*height*/
      2) && ll(e, "max-height", typeof /*height*/
      a[1] === void 0 ? "auto" : (
        /*height*/
        a[1] + "px"
      ));
    },
    i(a) {
      if (!i) {
        for (let r = 0; r < o.length; r += 1)
          dt(s[r]);
        i = !0;
      }
    },
    o(a) {
      s = s.filter(Boolean);
      for (let r = 0; r < s.length; r += 1)
        qt(s[r]);
      i = !1;
    },
    d(a) {
      a && xe(e), la(s, a);
    }
  };
}
function _a(n) {
  const e = n.lastIndexOf(".");
  return e === -1 ? [n, ""] : [n.slice(0, e), n.slice(e)];
}
function rl(n, e) {
  fetch(n).then((t) => t.text()).then((t) => {
    document.getElementById(e).innerText = t;
  }).catch((t) => console.error("Error while fetching file:", t));
}
function da(n, e, t) {
  let l;
  const i = ra();
  let { value: o } = e, { selectable: s = !1 } = e, { height: f = void 0 } = e, { i18n: a } = e;
  const r = (u, c) => i("select", { value: u.orig_name, index: c });
  return n.$$set = (u) => {
    "value" in u && t(5, o = u.value), "selectable" in u && t(0, s = u.selectable), "height" in u && t(1, f = u.height), "i18n" in u && t(2, a = u.i18n);
  }, n.$$.update = () => {
    n.$$.dirty & /*value*/
    32 && t(3, l = (Array.isArray(o) ? o : [o]).map((u) => {
      var c;
      const [d, _] = _a((c = u.orig_name) !== null && c !== void 0 ? c : "");
      return Object.assign(Object.assign({}, u), { filename_stem: d, filename_ext: _ });
    }));
  }, [s, f, a, l, i, o, r];
}
class ci extends ea {
  constructor(e) {
    super(), ia(this, e, da, ca, aa, {
      value: 5,
      selectable: 0,
      height: 1,
      i18n: 2
    });
  }
}
const {
  SvelteComponent: ma,
  bubble: ga,
  check_outros: ha,
  create_component: Xt,
  destroy_component: Yt,
  detach: fl,
  empty: pa,
  group_outros: ba,
  init: wa,
  insert: ul,
  mount_component: Qt,
  safe_not_equal: va,
  space: ka,
  transition_in: mt,
  transition_out: gt
} = window.__gradio__svelte__internal;
function ya(n) {
  let e, t;
  return e = new Go({
    props: {
      unpadded_box: !0,
      size: "large",
      $$slots: { default: [Sa] },
      $$scope: { ctx: n }
    }
  }), {
    c() {
      Xt(e.$$.fragment);
    },
    m(l, i) {
      Qt(e, l, i), t = !0;
    },
    p(l, i) {
      const o = {};
      i & /*$$scope*/
      128 && (o.$$scope = { dirty: i, ctx: l }), e.$set(o);
    },
    i(l) {
      t || (mt(e.$$.fragment, l), t = !0);
    },
    o(l) {
      gt(e.$$.fragment, l), t = !1;
    },
    d(l) {
      Yt(e, l);
    }
  };
}
function qa(n) {
  let e, t;
  return e = new ci({
    props: {
      i18n: (
        /*i18n*/
        n[5]
      ),
      selectable: (
        /*selectable*/
        n[3]
      ),
      value: (
        /*value*/
        n[0]
      ),
      height: (
        /*height*/
        n[4]
      )
    }
  }), e.$on(
    "select",
    /*select_handler*/
    n[6]
  ), {
    c() {
      Xt(e.$$.fragment);
    },
    m(l, i) {
      Qt(e, l, i), t = !0;
    },
    p(l, i) {
      const o = {};
      i & /*i18n*/
      32 && (o.i18n = /*i18n*/
      l[5]), i & /*selectable*/
      8 && (o.selectable = /*selectable*/
      l[3]), i & /*value*/
      1 && (o.value = /*value*/
      l[0]), i & /*height*/
      16 && (o.height = /*height*/
      l[4]), e.$set(o);
    },
    i(l) {
      t || (mt(e.$$.fragment, l), t = !0);
    },
    o(l) {
      gt(e.$$.fragment, l), t = !1;
    },
    d(l) {
      Yt(e, l);
    }
  };
}
function Sa(n) {
  let e, t;
  return e = new Un({}), {
    c() {
      Xt(e.$$.fragment);
    },
    m(l, i) {
      Qt(e, l, i), t = !0;
    },
    i(l) {
      t || (mt(e.$$.fragment, l), t = !0);
    },
    o(l) {
      gt(e.$$.fragment, l), t = !1;
    },
    d(l) {
      Yt(e, l);
    }
  };
}
function Ca(n) {
  let e, t, l, i, o, s, f;
  e = new li({
    props: {
      show_label: (
        /*show_label*/
        n[2]
      ),
      float: (
        /*value*/
        n[0] === null
      ),
      Icon: Un,
      label: (
        /*label*/
        n[1] || "File"
      )
    }
  });
  const a = [qa, ya], r = [];
  function u(c, d) {
    return d & /*value*/
    1 && (l = null), l == null && (l = !!/*value*/
    (c[0] && (!Array.isArray(
      /*value*/
      c[0]
    ) || /*value*/
    c[0].length > 0))), l ? 0 : 1;
  }
  return i = u(n, -1), o = r[i] = a[i](n), {
    c() {
      Xt(e.$$.fragment), t = ka(), o.c(), s = pa();
    },
    m(c, d) {
      Qt(e, c, d), ul(c, t, d), r[i].m(c, d), ul(c, s, d), f = !0;
    },
    p(c, [d]) {
      const _ = {};
      d & /*show_label*/
      4 && (_.show_label = /*show_label*/
      c[2]), d & /*value*/
      1 && (_.float = /*value*/
      c[0] === null), d & /*label*/
      2 && (_.label = /*label*/
      c[1] || "File"), e.$set(_);
      let m = i;
      i = u(c, d), i === m ? r[i].p(c, d) : (ba(), gt(r[m], 1, 1, () => {
        r[m] = null;
      }), ha(), o = r[i], o ? o.p(c, d) : (o = r[i] = a[i](c), o.c()), mt(o, 1), o.m(s.parentNode, s));
    },
    i(c) {
      f || (mt(e.$$.fragment, c), mt(o), f = !0);
    },
    o(c) {
      gt(e.$$.fragment, c), gt(o), f = !1;
    },
    d(c) {
      c && (fl(t), fl(s)), Yt(e, c), r[i].d(c);
    }
  };
}
function za(n, e, t) {
  let { value: l = null } = e, { label: i } = e, { show_label: o = !0 } = e, { selectable: s = !1 } = e, { height: f = void 0 } = e, { i18n: a } = e;
  function r(u) {
    ga.call(this, n, u);
  }
  return n.$$set = (u) => {
    "value" in u && t(0, l = u.value), "label" in u && t(1, i = u.label), "show_label" in u && t(2, o = u.show_label), "selectable" in u && t(3, s = u.selectable), "height" in u && t(4, f = u.height), "i18n" in u && t(5, a = u.i18n);
  }, [l, i, o, s, f, a, r];
}
class Da extends ma {
  constructor(e) {
    super(), wa(this, e, za, Ca, va, {
      value: 0,
      label: 1,
      show_label: 2,
      selectable: 3,
      height: 4,
      i18n: 5
    });
  }
}
var pn = new Intl.Collator(0, { numeric: 1 }).compare;
function cl(n, e, t) {
  return n = n.split("."), e = e.split("."), pn(n[0], e[0]) || pn(n[1], e[1]) || (e[2] = e.slice(2).join("."), t = /[.-]/.test(n[2] = n.slice(2).join(".")), t == /[.-]/.test(e[2]) ? pn(n[2], e[2]) : t ? -1 : 1);
}
function _i(n, e, t) {
  return e.startsWith("http://") || e.startsWith("https://") ? t ? n : e : n + e;
}
function bn(n) {
  if (n.startsWith("http")) {
    const { protocol: e, host: t } = new URL(n);
    return t.endsWith("hf.space") ? {
      ws_protocol: "wss",
      host: t,
      http_protocol: e
    } : {
      ws_protocol: e === "https:" ? "wss" : "ws",
      http_protocol: e,
      host: t
    };
  } else if (n.startsWith("file:"))
    return {
      ws_protocol: "ws",
      http_protocol: "http:",
      host: "lite.local"
      // Special fake hostname only used for this case. This matches the hostname allowed in `is_self_host()` in `js/wasm/network/host.ts`.
    };
  return {
    ws_protocol: "wss",
    http_protocol: "https:",
    host: n
  };
}
const di = /^[^\/]*\/[^\/]*$/, Ea = /.*hf\.space\/{0,1}$/;
async function ja(n, e) {
  const t = {};
  e && (t.Authorization = `Bearer ${e}`);
  const l = n.trim();
  if (di.test(l))
    try {
      const i = await fetch(
        `https://huggingface.co/api/spaces/${l}/host`,
        { headers: t }
      );
      if (i.status !== 200)
        throw new Error("Space metadata could not be loaded.");
      const o = (await i.json()).host;
      return {
        space_id: n,
        ...bn(o)
      };
    } catch (i) {
      throw new Error("Space metadata could not be loaded." + i.message);
    }
  if (Ea.test(l)) {
    const { ws_protocol: i, http_protocol: o, host: s } = bn(l);
    return {
      space_id: s.replace(".hf.space", ""),
      ws_protocol: i,
      http_protocol: o,
      host: s
    };
  }
  return {
    space_id: !1,
    ...bn(l)
  };
}
function Na(n) {
  let e = {};
  return n.forEach(({ api_name: t }, l) => {
    t && (e[t] = l);
  }), e;
}
const Fa = /^(?=[^]*\b[dD]iscussions{0,1}\b)(?=[^]*\b[dD]isabled\b)[^]*$/;
async function _l(n) {
  try {
    const t = (await fetch(
      `https://huggingface.co/api/spaces/${n}/discussions`,
      {
        method: "HEAD"
      }
    )).headers.get("x-error-message");
    return !(t && Fa.test(t));
  } catch {
    return !1;
  }
}
function Ye(n, e, t) {
  if (n == null)
    return null;
  if (Array.isArray(n)) {
    const l = [];
    for (const i of n)
      i == null ? l.push(null) : l.push(Ye(i, e, t));
    return l;
  }
  return n.is_stream ? t == null ? new ht({
    ...n,
    url: e + "/stream/" + n.path
  }) : new ht({
    ...n,
    url: "/proxy=" + t + "stream/" + n.path
  }) : new ht({
    ...n,
    url: La(n.path, e, t)
  });
}
function Aa(n) {
  try {
    const e = new URL(n);
    return e.protocol === "http:" || e.protocol === "https:";
  } catch {
    return !1;
  }
}
function La(n, e, t) {
  return n == null ? t ? `/proxy=${t}file=` : `${e}/file=` : Aa(n) ? n : t ? `/proxy=${t}file=${n}` : `${e}/file=${n}`;
}
async function Ba(n, e, t, l = Pa) {
  let i = (Array.isArray(n) ? n : [n]).map(
    (o) => o.blob
  );
  return await Promise.all(
    await l(e, i, void 0, t).then(
      async (o) => {
        if (o.error)
          throw new Error(o.error);
        return o.files ? o.files.map((s, f) => {
          const a = new ht({ ...n[f], path: s });
          return Ye(a, e, null);
        }) : [];
      }
    )
  );
}
async function Ia(n, e) {
  return n.map(
    (t, l) => new ht({
      path: t.name,
      orig_name: t.name,
      blob: t,
      size: t.size,
      mime_type: t.type,
      is_stream: e
    })
  );
}
class ht {
  constructor({
    path: e,
    url: t,
    orig_name: l,
    size: i,
    blob: o,
    is_stream: s,
    mime_type: f,
    alt_text: a
  }) {
    this.path = e, this.url = t, this.orig_name = l, this.size = i, this.blob = t ? void 0 : o, this.is_stream = s, this.mime_type = f, this.alt_text = a;
  }
}
const mi = "This application is too busy. Keep trying!", Re = "Connection errored out.";
let gi;
function Oa(n, e) {
  return { post_data: t, upload_files: l, client: i, handle_blob: o };
  async function t(s, f, a) {
    const r = { "Content-Type": "application/json" };
    a && (r.Authorization = `Bearer ${a}`);
    try {
      var u = await n(s, {
        method: "POST",
        body: JSON.stringify(f),
        headers: r
      });
    } catch {
      return [{ error: Re }, 500];
    }
    let c, d;
    try {
      c = await u.json(), d = u.status;
    } catch (_) {
      c = { error: `Could not parse server response: ${_}` }, d = 500;
    }
    return [c, d];
  }
  async function l(s, f, a, r) {
    const u = {};
    a && (u.Authorization = `Bearer ${a}`);
    const c = 1e3, d = [];
    for (let m = 0; m < f.length; m += c) {
      const y = f.slice(m, m + c), q = new FormData();
      y.forEach((p) => {
        q.append("files", p);
      });
      try {
        const p = r ? `${s}/upload?upload_id=${r}` : `${s}/upload`;
        var _ = await n(p, {
          method: "POST",
          body: q,
          headers: u
        });
      } catch {
        return { error: Re };
      }
      const w = await _.json();
      d.push(...w);
    }
    return { files: d };
  }
  async function i(s, f = { normalise_files: !0 }) {
    return new Promise(async (a) => {
      const { status_callback: r, hf_token: u, normalise_files: c } = f, d = {
        predict: te,
        submit: ae,
        view_api: Ne,
        component_server: ot
      }, _ = c ?? !0;
      if ((typeof window > "u" || !("WebSocket" in window)) && !global.Websocket) {
        const L = await import("./wrapper-6f348d45-B5bCGhfq.js");
        gi = (await import("./__vite-browser-external-DYxpcVy9.js")).Blob, global.WebSocket = L.WebSocket;
      }
      const { ws_protocol: m, http_protocol: y, host: q, space_id: w } = await ja(s, u), p = Math.random().toString(36).substring(2), h = {};
      let z = !1, F = {}, g = null;
      const D = {}, T = /* @__PURE__ */ new Set();
      let S, B = {}, I = !1;
      u && w && (I = await Ma(w, u));
      async function W(L) {
        if (S = L, B = Na(L?.dependencies || []), S.auth_required)
          return {
            config: S,
            ...d
          };
        try {
          G = await Ne(S);
        } catch (v) {
          console.error(`Could not get api details: ${v.message}`);
        }
        return {
          config: S,
          ...d
        };
      }
      let G;
      async function C(L) {
        if (r && r(L), L.status === "running")
          try {
            S = await hl(
              n,
              `${y}//${q}`,
              u
            );
            const v = await W(S);
            a(v);
          } catch (v) {
            console.error(v), r && r({
              status: "error",
              message: "Could not load this space.",
              load_status: "error",
              detail: "NOT_FOUND"
            });
          }
      }
      try {
        S = await hl(
          n,
          `${y}//${q}`,
          u
        );
        const L = await W(S);
        a(L);
      } catch (L) {
        console.error(L), w ? jn(
          w,
          di.test(w) ? "space_name" : "subdomain",
          C
        ) : r && r({
          status: "error",
          message: "Could not load this space.",
          load_status: "error",
          detail: "NOT_FOUND"
        });
      }
      function te(L, v, b) {
        let A = !1, k = !1, P;
        if (typeof L == "number")
          P = S.dependencies[L];
        else {
          const U = L.replace(/^\//, "");
          P = S.dependencies[B[U]];
        }
        if (P.types.continuous)
          throw new Error(
            "Cannot call predict on this function as it may run forever. Use submit instead"
          );
        return new Promise((U, Z) => {
          const ne = ae(L, v, b);
          let E;
          ne.on("data", (Q) => {
            k && (ne.destroy(), U(Q)), A = !0, E = Q;
          }).on("status", (Q) => {
            Q.stage === "error" && Z(Q), Q.stage === "complete" && (k = !0, A && (ne.destroy(), U(E)));
          });
        });
      }
      function ae(L, v, b, A = null) {
        let k, P;
        if (typeof L == "number")
          k = L, P = G.unnamed_endpoints[k];
        else {
          const x = L.replace(/^\//, "");
          k = B[x], P = G.named_endpoints[L.trim()];
        }
        if (typeof k != "number")
          throw new Error(
            "There is no endpoint matching that name of fn_index matching that number."
          );
        let U, Z, ne = S.protocol ?? "ws";
        const E = typeof L == "number" ? "/predict" : L;
        let Q, H = null, J = !1;
        const Fe = {};
        let Pe = "";
        typeof window < "u" && (Pe = new URLSearchParams(window.location.search).toString()), o(`${S.root}`, v, P, u).then(
          (x) => {
            if (Q = {
              data: x || [],
              event_data: b,
              fn_index: k,
              trigger_id: A
            }, Ta(k, S))
              M({
                type: "status",
                endpoint: E,
                stage: "pending",
                queue: !1,
                fn_index: k,
                time: /* @__PURE__ */ new Date()
              }), t(
                `${S.root}/run${E.startsWith("/") ? E : `/${E}`}${Pe ? "?" + Pe : ""}`,
                {
                  ...Q,
                  session_hash: p
                },
                u
              ).then(([K, Y]) => {
                const ve = _ ? Lt(
                  K.data,
                  P,
                  S.root,
                  S.root_url
                ) : K.data;
                Y == 200 ? (M({
                  type: "data",
                  endpoint: E,
                  fn_index: k,
                  data: ve,
                  time: /* @__PURE__ */ new Date()
                }), M({
                  type: "status",
                  endpoint: E,
                  fn_index: k,
                  stage: "complete",
                  eta: K.average_duration,
                  queue: !1,
                  time: /* @__PURE__ */ new Date()
                })) : M({
                  type: "status",
                  stage: "error",
                  endpoint: E,
                  fn_index: k,
                  message: K.error,
                  queue: !1,
                  time: /* @__PURE__ */ new Date()
                });
              }).catch((K) => {
                M({
                  type: "status",
                  stage: "error",
                  message: K.message,
                  endpoint: E,
                  fn_index: k,
                  queue: !1,
                  time: /* @__PURE__ */ new Date()
                });
              });
            else if (ne == "ws") {
              M({
                type: "status",
                stage: "pending",
                queue: !0,
                endpoint: E,
                fn_index: k,
                time: /* @__PURE__ */ new Date()
              });
              let K = new URL(`${m}://${_i(
                q,
                S.path,
                !0
              )}
							/queue/join${Pe ? "?" + Pe : ""}`);
              I && K.searchParams.set("__sign", I), U = new WebSocket(K), U.onclose = (Y) => {
                Y.wasClean || M({
                  type: "status",
                  stage: "error",
                  broken: !0,
                  message: Re,
                  queue: !0,
                  endpoint: E,
                  fn_index: k,
                  time: /* @__PURE__ */ new Date()
                });
              }, U.onmessage = function(Y) {
                const ve = JSON.parse(Y.data), { type: le, status: V, data: R } = wn(
                  ve,
                  h[k]
                );
                if (le === "update" && V && !J)
                  M({
                    type: "status",
                    endpoint: E,
                    fn_index: k,
                    time: /* @__PURE__ */ new Date(),
                    ...V
                  }), V.stage === "error" && U.close();
                else if (le === "hash") {
                  U.send(JSON.stringify({ fn_index: k, session_hash: p }));
                  return;
                } else le === "data" ? U.send(JSON.stringify({ ...Q, session_hash: p })) : le === "complete" ? J = V : le === "log" ? M({
                  type: "log",
                  log: R.log,
                  level: R.level,
                  endpoint: E,
                  fn_index: k
                }) : le === "generating" && M({
                  type: "status",
                  time: /* @__PURE__ */ new Date(),
                  ...V,
                  stage: V?.stage,
                  queue: !0,
                  endpoint: E,
                  fn_index: k
                });
                R && (M({
                  type: "data",
                  time: /* @__PURE__ */ new Date(),
                  data: _ ? Lt(
                    R.data,
                    P,
                    S.root,
                    S.root_url
                  ) : R.data,
                  endpoint: E,
                  fn_index: k
                }), J && (M({
                  type: "status",
                  time: /* @__PURE__ */ new Date(),
                  ...J,
                  stage: V?.stage,
                  queue: !0,
                  endpoint: E,
                  fn_index: k
                }), U.close()));
              }, cl(S.version || "2.0.0", "3.6") < 0 && addEventListener(
                "open",
                () => U.send(JSON.stringify({ hash: p }))
              );
            } else if (ne == "sse") {
              M({
                type: "status",
                stage: "pending",
                queue: !0,
                endpoint: E,
                fn_index: k,
                time: /* @__PURE__ */ new Date()
              });
              var de = new URLSearchParams({
                fn_index: k.toString(),
                session_hash: p
              }).toString();
              let K = new URL(
                `${S.root}/queue/join?${Pe ? Pe + "&" : ""}${de}`
              );
              Z = e(K), Z.onmessage = async function(Y) {
                const ve = JSON.parse(Y.data), { type: le, status: V, data: R } = wn(
                  ve,
                  h[k]
                );
                if (le === "update" && V && !J)
                  M({
                    type: "status",
                    endpoint: E,
                    fn_index: k,
                    time: /* @__PURE__ */ new Date(),
                    ...V
                  }), V.stage === "error" && Z.close();
                else if (le === "data") {
                  H = ve.event_id;
                  let [st, Ii] = await t(
                    `${S.root}/queue/data`,
                    {
                      ...Q,
                      session_hash: p,
                      event_id: H
                    },
                    u
                  );
                  Ii !== 200 && (M({
                    type: "status",
                    stage: "error",
                    message: Re,
                    queue: !0,
                    endpoint: E,
                    fn_index: k,
                    time: /* @__PURE__ */ new Date()
                  }), Z.close());
                } else le === "complete" ? J = V : le === "log" ? M({
                  type: "log",
                  log: R.log,
                  level: R.level,
                  endpoint: E,
                  fn_index: k
                }) : le === "generating" && M({
                  type: "status",
                  time: /* @__PURE__ */ new Date(),
                  ...V,
                  stage: V?.stage,
                  queue: !0,
                  endpoint: E,
                  fn_index: k
                });
                R && (M({
                  type: "data",
                  time: /* @__PURE__ */ new Date(),
                  data: _ ? Lt(
                    R.data,
                    P,
                    S.root,
                    S.root_url
                  ) : R.data,
                  endpoint: E,
                  fn_index: k
                }), J && (M({
                  type: "status",
                  time: /* @__PURE__ */ new Date(),
                  ...J,
                  stage: V?.stage,
                  queue: !0,
                  endpoint: E,
                  fn_index: k
                }), Z.close()));
              };
            } else ne == "sse_v1" && (M({
              type: "status",
              stage: "pending",
              queue: !0,
              endpoint: E,
              fn_index: k,
              time: /* @__PURE__ */ new Date()
            }), t(
              `${S.root}/queue/join?${Pe}`,
              {
                ...Q,
                session_hash: p
              },
              u
            ).then(([K, Y]) => {
              if (Y === 503)
                M({
                  type: "status",
                  stage: "error",
                  message: mi,
                  queue: !0,
                  endpoint: E,
                  fn_index: k,
                  time: /* @__PURE__ */ new Date()
                });
              else if (Y !== 200)
                M({
                  type: "status",
                  stage: "error",
                  message: Re,
                  queue: !0,
                  endpoint: E,
                  fn_index: k,
                  time: /* @__PURE__ */ new Date()
                });
              else {
                H = K.event_id;
                let ve = async function(le) {
                  try {
                    const { type: V, status: R, data: st } = wn(
                      le,
                      h[k]
                    );
                    if (V == "heartbeat")
                      return;
                    if (V === "update" && R && !J)
                      M({
                        type: "status",
                        endpoint: E,
                        fn_index: k,
                        time: /* @__PURE__ */ new Date(),
                        ...R
                      });
                    else if (V === "complete")
                      J = R;
                    else if (V == "unexpected_error")
                      console.error("Unexpected error", R?.message), M({
                        type: "status",
                        stage: "error",
                        message: R?.message || "An Unexpected Error Occurred!",
                        queue: !0,
                        endpoint: E,
                        fn_index: k,
                        time: /* @__PURE__ */ new Date()
                      });
                    else if (V === "log") {
                      M({
                        type: "log",
                        log: st.log,
                        level: st.level,
                        endpoint: E,
                        fn_index: k
                      });
                      return;
                    } else V === "generating" && M({
                      type: "status",
                      time: /* @__PURE__ */ new Date(),
                      ...R,
                      stage: R?.stage,
                      queue: !0,
                      endpoint: E,
                      fn_index: k
                    });
                    st && (M({
                      type: "data",
                      time: /* @__PURE__ */ new Date(),
                      data: _ ? Lt(
                        st.data,
                        P,
                        S.root,
                        S.root_url
                      ) : st.data,
                      endpoint: E,
                      fn_index: k
                    }), J && M({
                      type: "status",
                      time: /* @__PURE__ */ new Date(),
                      ...J,
                      stage: R?.stage,
                      queue: !0,
                      endpoint: E,
                      fn_index: k
                    })), (R?.stage === "complete" || R?.stage === "error") && D[H] && delete D[H];
                  } catch (V) {
                    console.error("Unexpected client exception", V), M({
                      type: "status",
                      stage: "error",
                      message: "An Unexpected Error Occurred!",
                      queue: !0,
                      endpoint: E,
                      fn_index: k,
                      time: /* @__PURE__ */ new Date()
                    }), Oe();
                  }
                };
                H in F && (F[H].forEach(
                  (le) => ve(le)
                ), delete F[H]), D[H] = ve, T.add(H), z || je();
              }
            }));
          }
        );
        function M(x) {
          const K = Fe[x.type] || [];
          K?.forEach((Y) => Y(x));
        }
        function en(x, de) {
          const K = Fe, Y = K[x] || [];
          return K[x] = Y, Y?.push(de), { on: en, off: Dt, cancel: tn, destroy: nn };
        }
        function Dt(x, de) {
          const K = Fe;
          let Y = K[x] || [];
          return Y = Y?.filter((ve) => ve !== de), K[x] = Y, { on: en, off: Dt, cancel: tn, destroy: nn };
        }
        async function tn() {
          const x = {
            stage: "complete",
            queue: !1,
            time: /* @__PURE__ */ new Date()
          };
          J = x, M({
            ...x,
            type: "status",
            endpoint: E,
            fn_index: k
          });
          let de = {};
          ne === "ws" ? (U && U.readyState === 0 ? U.addEventListener("open", () => {
            U.close();
          }) : U.close(), de = { fn_index: k, session_hash: p }) : (Z.close(), de = { event_id: H });
          try {
            await n(`${S.root}/reset`, {
              headers: { "Content-Type": "application/json" },
              method: "POST",
              body: JSON.stringify(de)
            });
          } catch {
            console.warn(
              "The `/reset` endpoint could not be called. Subsequent endpoint results may be unreliable."
            );
          }
        }
        function nn() {
          for (const x in Fe)
            Fe[x].forEach((de) => {
              Dt(x, de);
            });
        }
        return {
          on: en,
          off: Dt,
          cancel: tn,
          destroy: nn
        };
      }
      function je() {
        z = !0;
        let L = new URLSearchParams({
          session_hash: p
        }).toString(), v = new URL(`${S.root}/queue/data?${L}`);
        g = e(v), g.onmessage = async function(b) {
          let A = JSON.parse(b.data);
          const k = A.event_id;
          if (!k)
            await Promise.all(
              Object.keys(D).map(
                (P) => D[P](A)
              )
            );
          else if (D[k]) {
            A.msg === "process_completed" && (T.delete(k), T.size === 0 && Oe());
            let P = D[k];
            window.setTimeout(P, 0, A);
          } else
            F[k] || (F[k] = []), F[k].push(A);
        }, g.onerror = async function(b) {
          await Promise.all(
            Object.keys(D).map(
              (A) => D[A]({
                msg: "unexpected_error",
                message: Re
              })
            )
          ), Oe();
        };
      }
      function Oe() {
        z = !1, g?.close();
      }
      async function ot(L, v, b) {
        var A;
        const k = { "Content-Type": "application/json" };
        u && (k.Authorization = `Bearer ${u}`);
        let P, U = S.components.find(
          (E) => E.id === L
        );
        (A = U?.props) != null && A.root_url ? P = U.props.root_url : P = S.root;
        const Z = await n(
          `${P}/component_server/`,
          {
            method: "POST",
            body: JSON.stringify({
              data: b,
              component_id: L,
              fn_name: v,
              session_hash: p
            }),
            headers: k
          }
        );
        if (!Z.ok)
          throw new Error(
            "Could not connect to component server: " + Z.statusText
          );
        return await Z.json();
      }
      async function Ne(L) {
        if (G)
          return G;
        const v = { "Content-Type": "application/json" };
        u && (v.Authorization = `Bearer ${u}`);
        let b;
        if (cl(L.version || "2.0.0", "3.30") < 0 ? b = await n(
          "https://gradio-space-api-fetcher-v2.hf.space/api",
          {
            method: "POST",
            body: JSON.stringify({
              serialize: !1,
              config: JSON.stringify(L)
            }),
            headers: v
          }
        ) : b = await n(`${L.root}/info`, {
          headers: v
        }), !b.ok)
          throw new Error(Re);
        let A = await b.json();
        return "api" in A && (A = A.api), A.named_endpoints["/predict"] && !A.unnamed_endpoints[0] && (A.unnamed_endpoints[0] = A.named_endpoints["/predict"]), Ua(A, L, B);
      }
    });
  }
  async function o(s, f, a, r) {
    const u = await En(
      f,
      void 0,
      [],
      !0,
      a
    );
    return Promise.all(
      u.map(async ({ path: c, blob: d, type: _ }) => {
        if (d) {
          const m = (await l(s, [d], r)).files[0];
          return { path: c, file_url: m, type: _, name: d?.name };
        }
        return { path: c, type: _ };
      })
    ).then((c) => (c.forEach(({ path: d, file_url: _, type: m, name: y }) => {
      if (m === "Gallery")
        gl(f, _, d);
      else if (_) {
        const q = new ht({ path: _, orig_name: y });
        gl(f, q, d);
      }
    }), f));
  }
}
const { post_data: ju, upload_files: Pa, client: Nu, handle_blob: Fu } = Oa(
  fetch,
  (...n) => new EventSource(...n)
);
function Lt(n, e, t, l) {
  return n.map((i, o) => {
    var s, f, a, r;
    return ((f = (s = e?.returns) == null ? void 0 : s[o]) == null ? void 0 : f.component) === "File" ? Ye(i, t, l) : ((r = (a = e?.returns) == null ? void 0 : a[o]) == null ? void 0 : r.component) === "Gallery" ? i.map((u) => Array.isArray(u) ? [Ye(u[0], t, l), u[1]] : [Ye(u, t, l), null]) : typeof i == "object" && i.path ? Ye(i, t, l) : i;
  });
}
function dl(n, e, t, l) {
  switch (n.type) {
    case "string":
      return "string";
    case "boolean":
      return "boolean";
    case "number":
      return "number";
  }
  if (t === "JSONSerializable" || t === "StringSerializable")
    return "any";
  if (t === "ListStringSerializable")
    return "string[]";
  if (e === "Image")
    return l === "parameter" ? "Blob | File | Buffer" : "string";
  if (t === "FileSerializable")
    return n?.type === "array" ? l === "parameter" ? "(Blob | File | Buffer)[]" : "{ name: string; data: string; size?: number; is_file?: boolean; orig_name?: string}[]" : l === "parameter" ? "Blob | File | Buffer" : "{ name: string; data: string; size?: number; is_file?: boolean; orig_name?: string}";
  if (t === "GallerySerializable")
    return l === "parameter" ? "[(Blob | File | Buffer), (string | null)][]" : "[{ name: string; data: string; size?: number; is_file?: boolean; orig_name?: string}, (string | null))][]";
}
function ml(n, e) {
  return e === "GallerySerializable" ? "array of [file, label] tuples" : e === "ListStringSerializable" ? "array of strings" : e === "FileSerializable" ? "array of files or single file" : n.description;
}
function Ua(n, e, t) {
  const l = {
    named_endpoints: {},
    unnamed_endpoints: {}
  };
  for (const i in n) {
    const o = n[i];
    for (const s in o) {
      const f = e.dependencies[s] ? s : t[s.replace("/", "")], a = o[s];
      l[i][s] = {}, l[i][s].parameters = {}, l[i][s].returns = {}, l[i][s].type = e.dependencies[f].types, l[i][s].parameters = a.parameters.map(
        ({ label: r, component: u, type: c, serializer: d }) => ({
          label: r,
          component: u,
          type: dl(c, u, d, "parameter"),
          description: ml(c, d)
        })
      ), l[i][s].returns = a.returns.map(
        ({ label: r, component: u, type: c, serializer: d }) => ({
          label: r,
          component: u,
          type: dl(c, u, d, "return"),
          description: ml(c, d)
        })
      );
    }
  }
  return l;
}
async function Ma(n, e) {
  try {
    return (await (await fetch(`https://huggingface.co/api/spaces/${n}/jwt`, {
      headers: {
        Authorization: `Bearer ${e}`
      }
    })).json()).token || !1;
  } catch (t) {
    return console.error(t), !1;
  }
}
function gl(n, e, t) {
  for (; t.length > 1; )
    n = n[t.shift()];
  n[t.shift()] = e;
}
async function En(n, e = void 0, t = [], l = !1, i = void 0) {
  if (Array.isArray(n)) {
    let o = [];
    return await Promise.all(
      n.map(async (s, f) => {
        var a;
        let r = t.slice();
        r.push(f);
        const u = await En(
          n[f],
          l ? ((a = i?.parameters[f]) == null ? void 0 : a.component) || void 0 : e,
          r,
          !1,
          i
        );
        o = o.concat(u);
      })
    ), o;
  } else {
    if (globalThis.Buffer && n instanceof globalThis.Buffer)
      return [
        {
          path: t,
          blob: e === "Image" ? !1 : new gi([n]),
          type: e
        }
      ];
    if (typeof n == "object") {
      let o = [];
      for (let s in n)
        if (n.hasOwnProperty(s)) {
          let f = t.slice();
          f.push(s), o = o.concat(
            await En(
              n[s],
              void 0,
              f,
              !1,
              i
            )
          );
        }
      return o;
    }
  }
  return [];
}
function Ta(n, e) {
  var t, l, i, o;
  return !(((l = (t = e?.dependencies) == null ? void 0 : t[n]) == null ? void 0 : l.queue) === null ? e.enable_queue : (o = (i = e?.dependencies) == null ? void 0 : i[n]) != null && o.queue) || !1;
}
async function hl(n, e, t) {
  const l = {};
  if (t && (l.Authorization = `Bearer ${t}`), typeof window < "u" && window.gradio_config && location.origin !== "http://localhost:9876" && !window.gradio_config.dev_mode) {
    const i = window.gradio_config.root, o = window.gradio_config;
    return o.root = _i(e, o.root, !1), { ...o, path: i };
  } else if (e) {
    let i = await n(`${e}/config`, {
      headers: l
    });
    if (i.status === 200) {
      const o = await i.json();
      return o.path = o.path ?? "", o.root = e, o;
    }
    throw new Error("Could not get config.");
  }
  throw new Error("No config or app endpoint found");
}
async function jn(n, e, t) {
  let l = e === "subdomain" ? `https://huggingface.co/api/spaces/by-subdomain/${n}` : `https://huggingface.co/api/spaces/${n}`, i, o;
  try {
    if (i = await fetch(l), o = i.status, o !== 200)
      throw new Error();
    i = await i.json();
  } catch {
    t({
      status: "error",
      load_status: "error",
      message: "Could not get space status",
      detail: "NOT_FOUND"
    });
    return;
  }
  if (!i || o !== 200)
    return;
  const {
    runtime: { stage: s },
    id: f
  } = i;
  switch (s) {
    case "STOPPED":
    case "SLEEPING":
      t({
        status: "sleeping",
        load_status: "pending",
        message: "Space is asleep. Waking it up...",
        detail: s
      }), setTimeout(() => {
        jn(n, e, t);
      }, 1e3);
      break;
    case "PAUSED":
      t({
        status: "paused",
        load_status: "error",
        message: "This space has been paused by the author. If you would like to try this demo, consider duplicating the space.",
        detail: s,
        discussions_enabled: await _l(f)
      });
      break;
    case "RUNNING":
    case "RUNNING_BUILDING":
      t({
        status: "running",
        load_status: "complete",
        message: "",
        detail: s
      });
      break;
    case "BUILDING":
      t({
        status: "building",
        load_status: "pending",
        message: "Space is building...",
        detail: s
      }), setTimeout(() => {
        jn(n, e, t);
      }, 1e3);
      break;
    default:
      t({
        status: "space_error",
        load_status: "error",
        message: "This space is experiencing an issue.",
        detail: s,
        discussions_enabled: await _l(f)
      });
      break;
  }
}
function wn(n, e) {
  switch (n.msg) {
    case "send_data":
      return { type: "data" };
    case "send_hash":
      return { type: "hash" };
    case "queue_full":
      return {
        type: "update",
        status: {
          queue: !0,
          message: mi,
          stage: "error",
          code: n.code,
          success: n.success
        }
      };
    case "heartbeat":
      return {
        type: "heartbeat"
      };
    case "unexpected_error":
      return {
        type: "unexpected_error",
        status: {
          queue: !0,
          message: n.message,
          stage: "error",
          success: !1
        }
      };
    case "estimation":
      return {
        type: "update",
        status: {
          queue: !0,
          stage: e || "pending",
          code: n.code,
          size: n.queue_size,
          position: n.rank,
          eta: n.rank_eta,
          success: n.success
        }
      };
    case "progress":
      return {
        type: "update",
        status: {
          queue: !0,
          stage: "pending",
          code: n.code,
          progress_data: n.progress_data,
          success: n.success
        }
      };
    case "log":
      return { type: "log", data: n };
    case "process_generating":
      return {
        type: "generating",
        status: {
          queue: !0,
          message: n.success ? null : n.output.error,
          stage: n.success ? "generating" : "error",
          code: n.code,
          progress_data: n.progress_data,
          eta: n.average_duration
        },
        data: n.success ? n.output : null
      };
    case "process_completed":
      return "error" in n.output ? {
        type: "update",
        status: {
          queue: !0,
          message: n.output.error,
          stage: "error",
          code: n.code,
          success: n.success
        }
      } : {
        type: "complete",
        status: {
          queue: !0,
          message: n.success ? void 0 : n.output.error,
          stage: n.success ? "complete" : "error",
          code: n.code,
          progress_data: n.progress_data
        },
        data: n.success ? n.output : null
      };
    case "process_starts":
      return {
        type: "update",
        status: {
          queue: !0,
          stage: "pending",
          code: n.code,
          size: n.rank,
          position: 0,
          success: n.success,
          eta: n.eta
        }
      };
  }
  return { type: "none", status: { stage: "error", queue: !0 } };
}
const {
  SvelteComponent: Va,
  append: fe,
  attr: Ze,
  detach: hi,
  element: He,
  init: Ra,
  insert: pi,
  noop: pl,
  safe_not_equal: Wa,
  set_data: Jt,
  set_style: vn,
  space: Nn,
  text: ct,
  toggle_class: bl
} = window.__gradio__svelte__internal, { onMount: Ja, createEventDispatcher: Ga, getContext: Za } = window.__gradio__svelte__internal;
function wl(n) {
  let e, t, l, i, o = yt(
    /*file_to_display*/
    n[2]
  ) + "", s, f, a, r, u = (
    /*file_to_display*/
    n[2].orig_name + ""
  ), c;
  return {
    c() {
      e = He("div"), t = He("span"), l = He("div"), i = He("progress"), s = ct(o), a = Nn(), r = He("span"), c = ct(u), vn(i, "visibility", "hidden"), vn(i, "height", "0"), vn(i, "width", "0"), i.value = f = yt(
        /*file_to_display*/
        n[2]
      ), Ze(i, "max", "100"), Ze(i, "class", "svelte-12ckl9l"), Ze(l, "class", "progress-bar svelte-12ckl9l"), Ze(r, "class", "file-name svelte-12ckl9l"), Ze(e, "class", "file svelte-12ckl9l");
    },
    m(d, _) {
      pi(d, e, _), fe(e, t), fe(t, l), fe(l, i), fe(i, s), fe(e, a), fe(e, r), fe(r, c);
    },
    p(d, _) {
      _ & /*file_to_display*/
      4 && o !== (o = yt(
        /*file_to_display*/
        d[2]
      ) + "") && Jt(s, o), _ & /*file_to_display*/
      4 && f !== (f = yt(
        /*file_to_display*/
        d[2]
      )) && (i.value = f), _ & /*file_to_display*/
      4 && u !== (u = /*file_to_display*/
      d[2].orig_name + "") && Jt(c, u);
    },
    d(d) {
      d && hi(e);
    }
  };
}
function Ha(n) {
  let e, t, l, i = (
    /*files_with_progress*/
    n[0].length + ""
  ), o, s, f = (
    /*files_with_progress*/
    n[0].length > 1 ? "files" : "file"
  ), a, r, u, c = (
    /*file_to_display*/
    n[2] && wl(n)
  );
  return {
    c() {
      e = He("div"), t = He("span"), l = ct("Uploading "), o = ct(i), s = Nn(), a = ct(f), r = ct("..."), u = Nn(), c && c.c(), Ze(t, "class", "uploading svelte-12ckl9l"), Ze(e, "class", "wrap svelte-12ckl9l"), bl(
        e,
        "progress",
        /*progress*/
        n[1]
      );
    },
    m(d, _) {
      pi(d, e, _), fe(e, t), fe(t, l), fe(t, o), fe(t, s), fe(t, a), fe(t, r), fe(e, u), c && c.m(e, null);
    },
    p(d, [_]) {
      _ & /*files_with_progress*/
      1 && i !== (i = /*files_with_progress*/
      d[0].length + "") && Jt(o, i), _ & /*files_with_progress*/
      1 && f !== (f = /*files_with_progress*/
      d[0].length > 1 ? "files" : "file") && Jt(a, f), /*file_to_display*/
      d[2] ? c ? c.p(d, _) : (c = wl(d), c.c(), c.m(e, null)) : c && (c.d(1), c = null), _ & /*progress*/
      2 && bl(
        e,
        "progress",
        /*progress*/
        d[1]
      );
    },
    i: pl,
    o: pl,
    d(d) {
      d && hi(e), c && c.d();
    }
  };
}
function yt(n) {
  return n.progress * 100 / (n.size || 0) || 0;
}
function Ka(n) {
  let e = 0;
  return n.forEach((t) => {
    e += yt(t);
  }), document.documentElement.style.setProperty("--upload-progress-width", (e / n.length).toFixed(2) + "%"), e / n.length;
}
function Xa(n, e, t) {
  var l = this && this.__awaiter || function(y, q, w, p) {
    function h(z) {
      return z instanceof w ? z : new w(function(F) {
        F(z);
      });
    }
    return new (w || (w = Promise))(function(z, F) {
      function g(S) {
        try {
          T(p.next(S));
        } catch (B) {
          F(B);
        }
      }
      function D(S) {
        try {
          T(p.throw(S));
        } catch (B) {
          F(B);
        }
      }
      function T(S) {
        S.done ? z(S.value) : h(S.value).then(g, D);
      }
      T((p = p.apply(y, q || [])).next());
    });
  };
  let { upload_id: i } = e, { root: o } = e, { files: s } = e, f, a = !1, r, u, c = s.map((y) => Object.assign(Object.assign({}, y), { progress: 0 }));
  const d = Ga();
  function _(y, q) {
    t(0, c = c.map((w) => (w.orig_name === y && (w.progress += q), w)));
  }
  const m = Za("EventSource_factory");
  return Ja(() => {
    f = m(new URL(`${o}/upload_progress?upload_id=${i}`)), f.onmessage = function(y) {
      return l(this, void 0, void 0, function* () {
        const q = JSON.parse(y.data);
        a || t(1, a = !0), q.msg === "done" ? (f.close(), d("done")) : (t(6, r = q), _(q.orig_name, q.chunk_size));
      });
    };
  }), n.$$set = (y) => {
    "upload_id" in y && t(3, i = y.upload_id), "root" in y && t(4, o = y.root), "files" in y && t(5, s = y.files);
  }, n.$$.update = () => {
    n.$$.dirty & /*files_with_progress*/
    1 && Ka(c), n.$$.dirty & /*current_file_upload, files_with_progress*/
    65 && t(2, u = r || c[0]);
  }, [
    c,
    a,
    u,
    i,
    o,
    s,
    r
  ];
}
class Ya extends Va {
  constructor(e) {
    super(), Ra(this, e, Xa, Ha, Wa, { upload_id: 3, root: 4, files: 5 });
  }
}
const {
  SvelteComponent: Qa,
  append: vl,
  attr: oe,
  binding_callbacks: xa,
  bubble: We,
  check_outros: bi,
  create_component: $a,
  create_slot: wi,
  destroy_component: er,
  detach: xt,
  element: Fn,
  empty: vi,
  get_all_dirty_from_scope: ki,
  get_slot_changes: yi,
  group_outros: qi,
  init: tr,
  insert: $t,
  listen: ce,
  mount_component: nr,
  prevent_default: Je,
  run_all: lr,
  safe_not_equal: ir,
  set_style: Si,
  space: or,
  stop_propagation: Ge,
  toggle_class: se,
  transition_in: Ve,
  transition_out: it,
  update_slot_base: Ci
} = window.__gradio__svelte__internal, { createEventDispatcher: sr, tick: ar, getContext: rr } = window.__gradio__svelte__internal;
function fr(n) {
  let e, t, l, i, o, s, f, a, r, u;
  const c = (
    /*#slots*/
    n[22].default
  ), d = wi(
    c,
    n,
    /*$$scope*/
    n[21],
    null
  );
  return {
    c() {
      e = Fn("button"), d && d.c(), t = or(), l = Fn("input"), oe(l, "aria-label", "file upload"), oe(l, "data-testid", "file-upload"), oe(l, "type", "file"), oe(
        l,
        "accept",
        /*accept_file_types*/
        n[12]
      ), l.multiple = i = /*file_count*/
      n[5] === "multiple" || void 0, oe(l, "webkitdirectory", o = /*file_count*/
      n[5] === "directory" || void 0), oe(l, "mozdirectory", s = /*file_count*/
      n[5] === "directory" || void 0), oe(l, "class", "svelte-1aq8tno"), oe(e, "tabindex", f = /*hidden*/
      n[7] ? -1 : 0), oe(e, "class", "svelte-1aq8tno"), se(
        e,
        "hidden",
        /*hidden*/
        n[7]
      ), se(
        e,
        "center",
        /*center*/
        n[3]
      ), se(
        e,
        "boundedheight",
        /*boundedheight*/
        n[2]
      ), se(
        e,
        "flex",
        /*flex*/
        n[4]
      ), Si(e, "height", "100%");
    },
    m(_, m) {
      $t(_, e, m), d && d.m(e, null), vl(e, t), vl(e, l), n[30](l), a = !0, r || (u = [
        ce(
          l,
          "change",
          /*load_files_from_upload*/
          n[15]
        ),
        ce(e, "drag", Ge(Je(
          /*drag_handler*/
          n[23]
        ))),
        ce(e, "dragstart", Ge(Je(
          /*dragstart_handler*/
          n[24]
        ))),
        ce(e, "dragend", Ge(Je(
          /*dragend_handler*/
          n[25]
        ))),
        ce(e, "dragover", Ge(Je(
          /*dragover_handler*/
          n[26]
        ))),
        ce(e, "dragenter", Ge(Je(
          /*dragenter_handler*/
          n[27]
        ))),
        ce(e, "dragleave", Ge(Je(
          /*dragleave_handler*/
          n[28]
        ))),
        ce(e, "drop", Ge(Je(
          /*drop_handler*/
          n[29]
        ))),
        ce(
          e,
          "click",
          /*open_file_upload*/
          n[9]
        ),
        ce(
          e,
          "drop",
          /*loadFilesFromDrop*/
          n[16]
        ),
        ce(
          e,
          "dragenter",
          /*updateDragging*/
          n[14]
        ),
        ce(
          e,
          "dragleave",
          /*updateDragging*/
          n[14]
        )
      ], r = !0);
    },
    p(_, m) {
      d && d.p && (!a || m[0] & /*$$scope*/
      2097152) && Ci(
        d,
        c,
        _,
        /*$$scope*/
        _[21],
        a ? yi(
          c,
          /*$$scope*/
          _[21],
          m,
          null
        ) : ki(
          /*$$scope*/
          _[21]
        ),
        null
      ), (!a || m[0] & /*accept_file_types*/
      4096) && oe(
        l,
        "accept",
        /*accept_file_types*/
        _[12]
      ), (!a || m[0] & /*file_count*/
      32 && i !== (i = /*file_count*/
      _[5] === "multiple" || void 0)) && (l.multiple = i), (!a || m[0] & /*file_count*/
      32 && o !== (o = /*file_count*/
      _[5] === "directory" || void 0)) && oe(l, "webkitdirectory", o), (!a || m[0] & /*file_count*/
      32 && s !== (s = /*file_count*/
      _[5] === "directory" || void 0)) && oe(l, "mozdirectory", s), (!a || m[0] & /*hidden*/
      128 && f !== (f = /*hidden*/
      _[7] ? -1 : 0)) && oe(e, "tabindex", f), (!a || m[0] & /*hidden*/
      128) && se(
        e,
        "hidden",
        /*hidden*/
        _[7]
      ), (!a || m[0] & /*center*/
      8) && se(
        e,
        "center",
        /*center*/
        _[3]
      ), (!a || m[0] & /*boundedheight*/
      4) && se(
        e,
        "boundedheight",
        /*boundedheight*/
        _[2]
      ), (!a || m[0] & /*flex*/
      16) && se(
        e,
        "flex",
        /*flex*/
        _[4]
      );
    },
    i(_) {
      a || (Ve(d, _), a = !0);
    },
    o(_) {
      it(d, _), a = !1;
    },
    d(_) {
      _ && xt(e), d && d.d(_), n[30](null), r = !1, lr(u);
    }
  };
}
function ur(n) {
  let e, t, l = !/*hidden*/
  n[7] && kl(n);
  return {
    c() {
      l && l.c(), e = vi();
    },
    m(i, o) {
      l && l.m(i, o), $t(i, e, o), t = !0;
    },
    p(i, o) {
      /*hidden*/
      i[7] ? l && (qi(), it(l, 1, 1, () => {
        l = null;
      }), bi()) : l ? (l.p(i, o), o[0] & /*hidden*/
      128 && Ve(l, 1)) : (l = kl(i), l.c(), Ve(l, 1), l.m(e.parentNode, e));
    },
    i(i) {
      t || (Ve(l), t = !0);
    },
    o(i) {
      it(l), t = !1;
    },
    d(i) {
      i && xt(e), l && l.d(i);
    }
  };
}
function cr(n) {
  let e, t, l, i, o;
  const s = (
    /*#slots*/
    n[22].default
  ), f = wi(
    s,
    n,
    /*$$scope*/
    n[21],
    null
  );
  return {
    c() {
      e = Fn("button"), f && f.c(), oe(e, "tabindex", t = /*hidden*/
      n[7] ? -1 : 0), oe(e, "class", "svelte-1aq8tno"), se(
        e,
        "hidden",
        /*hidden*/
        n[7]
      ), se(
        e,
        "center",
        /*center*/
        n[3]
      ), se(
        e,
        "boundedheight",
        /*boundedheight*/
        n[2]
      ), se(
        e,
        "flex",
        /*flex*/
        n[4]
      ), Si(e, "height", "100%");
    },
    m(a, r) {
      $t(a, e, r), f && f.m(e, null), l = !0, i || (o = ce(
        e,
        "click",
        /*paste_clipboard*/
        n[8]
      ), i = !0);
    },
    p(a, r) {
      f && f.p && (!l || r[0] & /*$$scope*/
      2097152) && Ci(
        f,
        s,
        a,
        /*$$scope*/
        a[21],
        l ? yi(
          s,
          /*$$scope*/
          a[21],
          r,
          null
        ) : ki(
          /*$$scope*/
          a[21]
        ),
        null
      ), (!l || r[0] & /*hidden*/
      128 && t !== (t = /*hidden*/
      a[7] ? -1 : 0)) && oe(e, "tabindex", t), (!l || r[0] & /*hidden*/
      128) && se(
        e,
        "hidden",
        /*hidden*/
        a[7]
      ), (!l || r[0] & /*center*/
      8) && se(
        e,
        "center",
        /*center*/
        a[3]
      ), (!l || r[0] & /*boundedheight*/
      4) && se(
        e,
        "boundedheight",
        /*boundedheight*/
        a[2]
      ), (!l || r[0] & /*flex*/
      16) && se(
        e,
        "flex",
        /*flex*/
        a[4]
      );
    },
    i(a) {
      l || (Ve(f, a), l = !0);
    },
    o(a) {
      it(f, a), l = !1;
    },
    d(a) {
      a && xt(e), f && f.d(a), i = !1, o();
    }
  };
}
function kl(n) {
  let e, t;
  return e = new Ya({
    props: {
      root: (
        /*root*/
        n[6]
      ),
      upload_id: (
        /*upload_id*/
        n[10]
      ),
      files: (
        /*file_data*/
        n[11]
      )
    }
  }), {
    c() {
      $a(e.$$.fragment);
    },
    m(l, i) {
      nr(e, l, i), t = !0;
    },
    p(l, i) {
      const o = {};
      i[0] & /*root*/
      64 && (o.root = /*root*/
      l[6]), i[0] & /*upload_id*/
      1024 && (o.upload_id = /*upload_id*/
      l[10]), i[0] & /*file_data*/
      2048 && (o.files = /*file_data*/
      l[11]), e.$set(o);
    },
    i(l) {
      t || (Ve(e.$$.fragment, l), t = !0);
    },
    o(l) {
      it(e.$$.fragment, l), t = !1;
    },
    d(l) {
      er(e, l);
    }
  };
}
function _r(n) {
  let e, t, l, i;
  const o = [cr, ur, fr], s = [];
  function f(a, r) {
    return (
      /*filetype*/
      a[0] === "clipboard" ? 0 : (
        /*uploading*/
        a[1] ? 1 : 2
      )
    );
  }
  return e = f(n), t = s[e] = o[e](n), {
    c() {
      t.c(), l = vi();
    },
    m(a, r) {
      s[e].m(a, r), $t(a, l, r), i = !0;
    },
    p(a, r) {
      let u = e;
      e = f(a), e === u ? s[e].p(a, r) : (qi(), it(s[u], 1, 1, () => {
        s[u] = null;
      }), bi(), t = s[e], t ? t.p(a, r) : (t = s[e] = o[e](a), t.c()), Ve(t, 1), t.m(l.parentNode, l));
    },
    i(a) {
      i || (Ve(t), i = !0);
    },
    o(a) {
      it(t), i = !1;
    },
    d(a) {
      a && xt(l), s[e].d(a);
    }
  };
}
function dr(n, e) {
  return !n || n === "*" || n === "file/*" ? !0 : (typeof n == "string" && n.endsWith("/*") && (n = n.split(",")), Array.isArray(n) ? n.includes(e) || n.some((t) => {
    const [l] = t.split("/");
    return t.endsWith("/*") && e.startsWith(l + "/");
  }) : n === e);
}
function mr(n, e, t) {
  let { $$slots: l = {}, $$scope: i } = e;
  var o = this && this.__awaiter || function(v, b, A, k) {
    function P(U) {
      return U instanceof A ? U : new A(function(Z) {
        Z(U);
      });
    }
    return new (A || (A = Promise))(function(U, Z) {
      function ne(H) {
        try {
          Q(k.next(H));
        } catch (J) {
          Z(J);
        }
      }
      function E(H) {
        try {
          Q(k.throw(H));
        } catch (J) {
          Z(J);
        }
      }
      function Q(H) {
        H.done ? U(H.value) : P(H.value).then(ne, E);
      }
      Q((k = k.apply(v, b || [])).next());
    });
  };
  let { filetype: s = null } = e, { dragging: f = !1 } = e, { boundedheight: a = !0 } = e, { center: r = !0 } = e, { flex: u = !0 } = e, { file_count: c = "single" } = e, { disable_click: d = !1 } = e, { root: _ } = e, { hidden: m = !1 } = e, { format: y = "file" } = e, { uploading: q = !1 } = e, w, p, h;
  const z = rr("upload_files");
  let F;
  const g = sr();
  function D() {
    t(17, f = !f);
  }
  function T() {
    navigator.clipboard.read().then((v) => o(this, void 0, void 0, function* () {
      for (let b = 0; b < v.length; b++) {
        const A = v[b].types.find((k) => k.startsWith("image/"));
        if (A) {
          v[b].getType(A).then((k) => o(this, void 0, void 0, function* () {
            const P = new File([k], `clipboard.${A.replace("image/", "")}`);
            yield I([P]);
          }));
          break;
        }
      }
    }));
  }
  function S() {
    d || (t(13, F.value = "", F), F.click());
  }
  function B(v) {
    return o(this, void 0, void 0, function* () {
      yield ar(), t(10, w = Math.random().toString(36).substring(2, 15)), t(1, q = !0);
      const b = yield Ba(v, _, w, z);
      return g("load", c === "single" ? b?.[0] : b), t(1, q = !1), b || [];
    });
  }
  function I(v) {
    return o(this, void 0, void 0, function* () {
      if (!v.length)
        return;
      let b = v.map((A) => new File([A], A.name));
      return t(11, p = yield Ia(b)), yield B(p);
    });
  }
  function W(v) {
    return o(this, void 0, void 0, function* () {
      const b = v.target;
      if (b.files)
        if (y != "blob")
          yield I(Array.from(b.files));
        else {
          if (c === "single") {
            g("load", b.files[0]);
            return;
          }
          g("load", b.files);
        }
    });
  }
  function G(v) {
    return o(this, void 0, void 0, function* () {
      var b;
      if (t(17, f = !1), !(!((b = v.dataTransfer) === null || b === void 0) && b.files)) return;
      const A = Array.from(v.dataTransfer.files).filter((k) => {
        const P = "." + k.name.split(".").pop();
        return k.type && dr(s, k.type) || (P && Array.isArray(s) ? s.includes(P) : P === s) ? !0 : (g("error", `Invalid file type only ${s} allowed.`), !1);
      });
      yield I(A);
    });
  }
  function C(v) {
    We.call(this, n, v);
  }
  function te(v) {
    We.call(this, n, v);
  }
  function ae(v) {
    We.call(this, n, v);
  }
  function je(v) {
    We.call(this, n, v);
  }
  function Oe(v) {
    We.call(this, n, v);
  }
  function ot(v) {
    We.call(this, n, v);
  }
  function Ne(v) {
    We.call(this, n, v);
  }
  function L(v) {
    xa[v ? "unshift" : "push"](() => {
      F = v, t(13, F);
    });
  }
  return n.$$set = (v) => {
    "filetype" in v && t(0, s = v.filetype), "dragging" in v && t(17, f = v.dragging), "boundedheight" in v && t(2, a = v.boundedheight), "center" in v && t(3, r = v.center), "flex" in v && t(4, u = v.flex), "file_count" in v && t(5, c = v.file_count), "disable_click" in v && t(18, d = v.disable_click), "root" in v && t(6, _ = v.root), "hidden" in v && t(7, m = v.hidden), "format" in v && t(19, y = v.format), "uploading" in v && t(1, q = v.uploading), "$$scope" in v && t(21, i = v.$$scope);
  }, n.$$.update = () => {
    n.$$.dirty[0] & /*filetype*/
    1 && (s == null || typeof s == "string" ? t(12, h = s) : (t(0, s = s.map((v) => v.startsWith(".") ? v : v + "/*")), t(12, h = s.join(", "))));
  }, [
    s,
    q,
    a,
    r,
    u,
    c,
    _,
    m,
    T,
    S,
    w,
    p,
    h,
    F,
    D,
    W,
    G,
    f,
    d,
    y,
    I,
    i,
    l,
    C,
    te,
    ae,
    je,
    Oe,
    ot,
    Ne,
    L
  ];
}
class gr extends Qa {
  constructor(e) {
    super(), tr(
      this,
      e,
      mr,
      _r,
      ir,
      {
        filetype: 0,
        dragging: 17,
        boundedheight: 2,
        center: 3,
        flex: 4,
        file_count: 5,
        disable_click: 18,
        root: 6,
        hidden: 7,
        format: 19,
        uploading: 1,
        paste_clipboard: 8,
        open_file_upload: 9,
        load_files: 20
      },
      null,
      [-1, -1]
    );
  }
  get paste_clipboard() {
    return this.$$.ctx[8];
  }
  get open_file_upload() {
    return this.$$.ctx[9];
  }
  get load_files() {
    return this.$$.ctx[20];
  }
}
const {
  SvelteComponent: hr,
  append: An,
  attr: Le,
  bubble: pr,
  create_component: br,
  destroy_component: wr,
  detach: zi,
  element: Ln,
  init: vr,
  insert: Di,
  listen: kr,
  mount_component: yr,
  safe_not_equal: qr,
  set_data: Sr,
  set_style: Bt,
  space: Cr,
  text: zr,
  toggle_class: he,
  transition_in: Dr,
  transition_out: Er
} = window.__gradio__svelte__internal;
function yl(n) {
  let e, t;
  return {
    c() {
      e = Ln("span"), t = zr(
        /*label*/
        n[1]
      ), Le(e, "class", "svelte-lpi64a");
    },
    m(l, i) {
      Di(l, e, i), An(e, t);
    },
    p(l, i) {
      i & /*label*/
      2 && Sr(
        t,
        /*label*/
        l[1]
      );
    },
    d(l) {
      l && zi(e);
    }
  };
}
function jr(n) {
  let e, t, l, i, o, s, f, a = (
    /*show_label*/
    n[2] && yl(n)
  );
  return i = new /*Icon*/
  n[0]({}), {
    c() {
      e = Ln("button"), a && a.c(), t = Cr(), l = Ln("div"), br(i.$$.fragment), Le(l, "class", "svelte-lpi64a"), he(
        l,
        "small",
        /*size*/
        n[4] === "small"
      ), he(
        l,
        "large",
        /*size*/
        n[4] === "large"
      ), e.disabled = /*disabled*/
      n[7], Le(
        e,
        "aria-label",
        /*label*/
        n[1]
      ), Le(
        e,
        "aria-haspopup",
        /*hasPopup*/
        n[8]
      ), Le(
        e,
        "title",
        /*label*/
        n[1]
      ), Le(e, "class", "svelte-lpi64a"), he(
        e,
        "pending",
        /*pending*/
        n[3]
      ), he(
        e,
        "padded",
        /*padded*/
        n[5]
      ), he(
        e,
        "highlight",
        /*highlight*/
        n[6]
      ), he(
        e,
        "transparent",
        /*transparent*/
        n[9]
      ), Bt(e, "color", !/*disabled*/
      n[7] && /*_color*/
      n[11] ? (
        /*_color*/
        n[11]
      ) : "var(--block-label-text-color)"), Bt(e, "--bg-color", /*disabled*/
      n[7] ? "auto" : (
        /*background*/
        n[10]
      ));
    },
    m(r, u) {
      Di(r, e, u), a && a.m(e, null), An(e, t), An(e, l), yr(i, l, null), o = !0, s || (f = kr(
        e,
        "click",
        /*click_handler*/
        n[13]
      ), s = !0);
    },
    p(r, [u]) {
      /*show_label*/
      r[2] ? a ? a.p(r, u) : (a = yl(r), a.c(), a.m(e, t)) : a && (a.d(1), a = null), (!o || u & /*size*/
      16) && he(
        l,
        "small",
        /*size*/
        r[4] === "small"
      ), (!o || u & /*size*/
      16) && he(
        l,
        "large",
        /*size*/
        r[4] === "large"
      ), (!o || u & /*disabled*/
      128) && (e.disabled = /*disabled*/
      r[7]), (!o || u & /*label*/
      2) && Le(
        e,
        "aria-label",
        /*label*/
        r[1]
      ), (!o || u & /*hasPopup*/
      256) && Le(
        e,
        "aria-haspopup",
        /*hasPopup*/
        r[8]
      ), (!o || u & /*label*/
      2) && Le(
        e,
        "title",
        /*label*/
        r[1]
      ), (!o || u & /*pending*/
      8) && he(
        e,
        "pending",
        /*pending*/
        r[3]
      ), (!o || u & /*padded*/
      32) && he(
        e,
        "padded",
        /*padded*/
        r[5]
      ), (!o || u & /*highlight*/
      64) && he(
        e,
        "highlight",
        /*highlight*/
        r[6]
      ), (!o || u & /*transparent*/
      512) && he(
        e,
        "transparent",
        /*transparent*/
        r[9]
      ), u & /*disabled, _color*/
      2176 && Bt(e, "color", !/*disabled*/
      r[7] && /*_color*/
      r[11] ? (
        /*_color*/
        r[11]
      ) : "var(--block-label-text-color)"), u & /*disabled, background*/
      1152 && Bt(e, "--bg-color", /*disabled*/
      r[7] ? "auto" : (
        /*background*/
        r[10]
      ));
    },
    i(r) {
      o || (Dr(i.$$.fragment, r), o = !0);
    },
    o(r) {
      Er(i.$$.fragment, r), o = !1;
    },
    d(r) {
      r && zi(e), a && a.d(), wr(i), s = !1, f();
    }
  };
}
function Nr(n, e, t) {
  let l, { Icon: i } = e, { label: o = "" } = e, { show_label: s = !1 } = e, { pending: f = !1 } = e, { size: a = "small" } = e, { padded: r = !0 } = e, { highlight: u = !1 } = e, { disabled: c = !1 } = e, { hasPopup: d = !1 } = e, { color: _ = "var(--block-label-text-color)" } = e, { transparent: m = !1 } = e, { background: y = "var(--background-fill-primary)" } = e;
  function q(w) {
    pr.call(this, n, w);
  }
  return n.$$set = (w) => {
    "Icon" in w && t(0, i = w.Icon), "label" in w && t(1, o = w.label), "show_label" in w && t(2, s = w.show_label), "pending" in w && t(3, f = w.pending), "size" in w && t(4, a = w.size), "padded" in w && t(5, r = w.padded), "highlight" in w && t(6, u = w.highlight), "disabled" in w && t(7, c = w.disabled), "hasPopup" in w && t(8, d = w.hasPopup), "color" in w && t(12, _ = w.color), "transparent" in w && t(9, m = w.transparent), "background" in w && t(10, y = w.background);
  }, n.$$.update = () => {
    n.$$.dirty & /*highlight, color*/
    4160 && t(11, l = u ? "var(--color-accent)" : _);
  }, [
    i,
    o,
    s,
    f,
    a,
    r,
    u,
    c,
    d,
    m,
    y,
    l,
    _,
    q
  ];
}
class Mn extends hr {
  constructor(e) {
    super(), vr(this, e, Nr, jr, qr, {
      Icon: 0,
      label: 1,
      show_label: 2,
      pending: 3,
      size: 4,
      padded: 5,
      highlight: 6,
      disabled: 7,
      hasPopup: 8,
      color: 12,
      transparent: 9,
      background: 10
    });
  }
}
const {
  SvelteComponent: Fr,
  append: ql,
  attr: Ar,
  check_outros: Sl,
  create_component: Tn,
  destroy_component: Vn,
  detach: Lr,
  element: Br,
  group_outros: Cl,
  init: Ir,
  insert: Or,
  mount_component: Rn,
  safe_not_equal: Pr,
  set_style: zl,
  space: Dl,
  toggle_class: El,
  transition_in: Be,
  transition_out: Ke
} = window.__gradio__svelte__internal, { createEventDispatcher: Ur } = window.__gradio__svelte__internal;
function jl(n) {
  let e, t;
  return e = new Mn({
    props: {
      Icon: Ts,
      label: (
        /*i18n*/
        n[3]("common.edit")
      )
    }
  }), e.$on(
    "click",
    /*click_handler*/
    n[5]
  ), {
    c() {
      Tn(e.$$.fragment);
    },
    m(l, i) {
      Rn(e, l, i), t = !0;
    },
    p(l, i) {
      const o = {};
      i & /*i18n*/
      8 && (o.label = /*i18n*/
      l[3]("common.edit")), e.$set(o);
    },
    i(l) {
      t || (Be(e.$$.fragment, l), t = !0);
    },
    o(l) {
      Ke(e.$$.fragment, l), t = !1;
    },
    d(l) {
      Vn(e, l);
    }
  };
}
function Nl(n) {
  let e, t;
  return e = new Mn({
    props: {
      Icon: $s,
      label: (
        /*i18n*/
        n[3]("common.undo")
      )
    }
  }), e.$on(
    "click",
    /*click_handler_1*/
    n[6]
  ), {
    c() {
      Tn(e.$$.fragment);
    },
    m(l, i) {
      Rn(e, l, i), t = !0;
    },
    p(l, i) {
      const o = {};
      i & /*i18n*/
      8 && (o.label = /*i18n*/
      l[3]("common.undo")), e.$set(o);
    },
    i(l) {
      t || (Be(e.$$.fragment, l), t = !0);
    },
    o(l) {
      Ke(e.$$.fragment, l), t = !1;
    },
    d(l) {
      Vn(e, l);
    }
  };
}
function Mr(n) {
  let e, t, l, i, o, s = (
    /*editable*/
    n[0] && jl(n)
  ), f = (
    /*undoable*/
    n[1] && Nl(n)
  );
  return i = new Mn({
    props: {
      Icon: Ss,
      label: (
        /*i18n*/
        n[3]("common.clear")
      )
    }
  }), i.$on(
    "click",
    /*click_handler_2*/
    n[7]
  ), {
    c() {
      e = Br("div"), s && s.c(), t = Dl(), f && f.c(), l = Dl(), Tn(i.$$.fragment), Ar(e, "class", "svelte-1wj0ocy"), El(e, "not-absolute", !/*absolute*/
      n[2]), zl(
        e,
        "position",
        /*absolute*/
        n[2] ? "absolute" : "static"
      );
    },
    m(a, r) {
      Or(a, e, r), s && s.m(e, null), ql(e, t), f && f.m(e, null), ql(e, l), Rn(i, e, null), o = !0;
    },
    p(a, [r]) {
      /*editable*/
      a[0] ? s ? (s.p(a, r), r & /*editable*/
      1 && Be(s, 1)) : (s = jl(a), s.c(), Be(s, 1), s.m(e, t)) : s && (Cl(), Ke(s, 1, 1, () => {
        s = null;
      }), Sl()), /*undoable*/
      a[1] ? f ? (f.p(a, r), r & /*undoable*/
      2 && Be(f, 1)) : (f = Nl(a), f.c(), Be(f, 1), f.m(e, l)) : f && (Cl(), Ke(f, 1, 1, () => {
        f = null;
      }), Sl());
      const u = {};
      r & /*i18n*/
      8 && (u.label = /*i18n*/
      a[3]("common.clear")), i.$set(u), (!o || r & /*absolute*/
      4) && El(e, "not-absolute", !/*absolute*/
      a[2]), r & /*absolute*/
      4 && zl(
        e,
        "position",
        /*absolute*/
        a[2] ? "absolute" : "static"
      );
    },
    i(a) {
      o || (Be(s), Be(f), Be(i.$$.fragment, a), o = !0);
    },
    o(a) {
      Ke(s), Ke(f), Ke(i.$$.fragment, a), o = !1;
    },
    d(a) {
      a && Lr(e), s && s.d(), f && f.d(), Vn(i);
    }
  };
}
function Tr(n, e, t) {
  let { editable: l = !1 } = e, { undoable: i = !1 } = e, { absolute: o = !0 } = e, { i18n: s } = e;
  const f = Ur(), a = () => f("edit"), r = () => f("undo"), u = (c) => {
    f("clear"), c.stopPropagation();
  };
  return n.$$set = (c) => {
    "editable" in c && t(0, l = c.editable), "undoable" in c && t(1, i = c.undoable), "absolute" in c && t(2, o = c.absolute), "i18n" in c && t(3, s = c.i18n);
  }, [
    l,
    i,
    o,
    s,
    f,
    a,
    r,
    u
  ];
}
class Vr extends Fr {
  constructor(e) {
    super(), Ir(this, e, Tr, Mr, Pr, {
      editable: 0,
      undoable: 1,
      absolute: 2,
      i18n: 3
    });
  }
}
const {
  SvelteComponent: Rr,
  add_flush_callback: Wr,
  bind: Jr,
  binding_callbacks: Gr,
  bubble: Zr,
  check_outros: Hr,
  create_component: Gt,
  create_slot: Kr,
  destroy_component: Zt,
  detach: Bn,
  empty: Xr,
  get_all_dirty_from_scope: Yr,
  get_slot_changes: Qr,
  group_outros: xr,
  init: $r,
  insert: In,
  mount_component: Ht,
  safe_not_equal: ef,
  space: Ei,
  transition_in: et,
  transition_out: tt,
  update_slot_base: tf
} = window.__gradio__svelte__internal, { createEventDispatcher: nf, tick: lf } = window.__gradio__svelte__internal;
function of(n) {
  let e, t, l;
  function i(s) {
    n[15](s);
  }
  let o = {
    filetype: (
      /*accept_file_types*/
      n[9]
    ),
    file_count: (
      /*file_count*/
      n[3]
    ),
    root: (
      /*root*/
      n[5]
    ),
    $$slots: { default: [af] },
    $$scope: { ctx: n }
  };
  return (
    /*dragging*/
    n[8] !== void 0 && (o.dragging = /*dragging*/
    n[8]), e = new gr({ props: o }), Gr.push(() => Jr(e, "dragging", i)), e.$on(
      "load",
      /*handle_upload*/
      n[10]
    ), {
      c() {
        Gt(e.$$.fragment);
      },
      m(s, f) {
        Ht(e, s, f), l = !0;
      },
      p(s, f) {
        const a = {};
        f & /*accept_file_types*/
        512 && (a.filetype = /*accept_file_types*/
        s[9]), f & /*file_count*/
        8 && (a.file_count = /*file_count*/
        s[3]), f & /*root*/
        32 && (a.root = /*root*/
        s[5]), f & /*$$scope*/
        65536 && (a.$$scope = { dirty: f, ctx: s }), !t && f & /*dragging*/
        256 && (t = !0, a.dragging = /*dragging*/
        s[8], Wr(() => t = !1)), e.$set(a);
      },
      i(s) {
        l || (et(e.$$.fragment, s), l = !0);
      },
      o(s) {
        tt(e.$$.fragment, s), l = !1;
      },
      d(s) {
        Zt(e, s);
      }
    }
  );
}
function sf(n) {
  let e, t, l, i;
  return e = new Vr({
    props: { i18n: (
      /*i18n*/
      n[7]
    ), absolute: !0 }
  }), e.$on(
    "clear",
    /*handle_clear*/
    n[11]
  ), l = new ci({
    props: {
      i18n: (
        /*i18n*/
        n[7]
      ),
      selectable: (
        /*selectable*/
        n[4]
      ),
      value: (
        /*value*/
        n[0]
      ),
      height: (
        /*height*/
        n[6]
      )
    }
  }), l.$on(
    "select",
    /*select_handler*/
    n[14]
  ), {
    c() {
      Gt(e.$$.fragment), t = Ei(), Gt(l.$$.fragment);
    },
    m(o, s) {
      Ht(e, o, s), In(o, t, s), Ht(l, o, s), i = !0;
    },
    p(o, s) {
      const f = {};
      s & /*i18n*/
      128 && (f.i18n = /*i18n*/
      o[7]), e.$set(f);
      const a = {};
      s & /*i18n*/
      128 && (a.i18n = /*i18n*/
      o[7]), s & /*selectable*/
      16 && (a.selectable = /*selectable*/
      o[4]), s & /*value*/
      1 && (a.value = /*value*/
      o[0]), s & /*height*/
      64 && (a.height = /*height*/
      o[6]), l.$set(a);
    },
    i(o) {
      i || (et(e.$$.fragment, o), et(l.$$.fragment, o), i = !0);
    },
    o(o) {
      tt(e.$$.fragment, o), tt(l.$$.fragment, o), i = !1;
    },
    d(o) {
      o && Bn(t), Zt(e, o), Zt(l, o);
    }
  };
}
function af(n) {
  let e;
  const t = (
    /*#slots*/
    n[13].default
  ), l = Kr(
    t,
    n,
    /*$$scope*/
    n[16],
    null
  );
  return {
    c() {
      l && l.c();
    },
    m(i, o) {
      l && l.m(i, o), e = !0;
    },
    p(i, o) {
      l && l.p && (!e || o & /*$$scope*/
      65536) && tf(
        l,
        t,
        i,
        /*$$scope*/
        i[16],
        e ? Qr(
          t,
          /*$$scope*/
          i[16],
          o,
          null
        ) : Yr(
          /*$$scope*/
          i[16]
        ),
        null
      );
    },
    i(i) {
      e || (et(l, i), e = !0);
    },
    o(i) {
      tt(l, i), e = !1;
    },
    d(i) {
      l && l.d(i);
    }
  };
}
function rf(n) {
  let e, t, l, i, o, s;
  e = new li({
    props: {
      show_label: (
        /*show_label*/
        n[2]
      ),
      Icon: Un,
      float: (
        /*value*/
        n[0] === null
      ),
      label: (
        /*label*/
        n[1] || "File"
      )
    }
  });
  const f = [sf, of], a = [];
  function r(u, c) {
    return (
      /*value*/
      u[0] ? 0 : 1
    );
  }
  return l = r(n), i = a[l] = f[l](n), {
    c() {
      Gt(e.$$.fragment), t = Ei(), i.c(), o = Xr();
    },
    m(u, c) {
      Ht(e, u, c), In(u, t, c), a[l].m(u, c), In(u, o, c), s = !0;
    },
    p(u, [c]) {
      const d = {};
      c & /*show_label*/
      4 && (d.show_label = /*show_label*/
      u[2]), c & /*value*/
      1 && (d.float = /*value*/
      u[0] === null), c & /*label*/
      2 && (d.label = /*label*/
      u[1] || "File"), e.$set(d);
      let _ = l;
      l = r(u), l === _ ? a[l].p(u, c) : (xr(), tt(a[_], 1, 1, () => {
        a[_] = null;
      }), Hr(), i = a[l], i ? i.p(u, c) : (i = a[l] = f[l](u), i.c()), et(i, 1), i.m(o.parentNode, o));
    },
    i(u) {
      s || (et(e.$$.fragment, u), et(i), s = !0);
    },
    o(u) {
      tt(e.$$.fragment, u), tt(i), s = !1;
    },
    d(u) {
      u && (Bn(t), Bn(o)), Zt(e, u), a[l].d(u);
    }
  };
}
function ff(n, e, t) {
  let { $$slots: l = {}, $$scope: i } = e;
  var o = this && this.__awaiter || function(g, D, T, S) {
    function B(I) {
      return I instanceof T ? I : new T(function(W) {
        W(I);
      });
    }
    return new (T || (T = Promise))(function(I, W) {
      function G(ae) {
        try {
          te(S.next(ae));
        } catch (je) {
          W(je);
        }
      }
      function C(ae) {
        try {
          te(S.throw(ae));
        } catch (je) {
          W(je);
        }
      }
      function te(ae) {
        ae.done ? I(ae.value) : B(ae.value).then(G, C);
      }
      te((S = S.apply(g, D || [])).next());
    });
  };
  let { value: s } = e, { label: f } = e, { show_label: a = !0 } = e, { file_count: r = "single" } = e, { file_types: u = null } = e, { selectable: c = !1 } = e, { root: d } = e, { height: _ = void 0 } = e, { i18n: m } = e;
  function y(g) {
    return o(this, arguments, void 0, function* ({ detail: D }) {
      t(0, s = D), yield lf(), w("change", s), w("upload", D);
    });
  }
  function q() {
    t(0, s = null), w("change", null), w("clear");
  }
  const w = nf();
  let p;
  u == null ? p = null : (u = u.map((g) => g.startsWith(".") ? g : g + "/*"), p = u.join(", "));
  let h = !1;
  function z(g) {
    Zr.call(this, n, g);
  }
  function F(g) {
    h = g, t(8, h);
  }
  return n.$$set = (g) => {
    "value" in g && t(0, s = g.value), "label" in g && t(1, f = g.label), "show_label" in g && t(2, a = g.show_label), "file_count" in g && t(3, r = g.file_count), "file_types" in g && t(12, u = g.file_types), "selectable" in g && t(4, c = g.selectable), "root" in g && t(5, d = g.root), "height" in g && t(6, _ = g.height), "i18n" in g && t(7, m = g.i18n), "$$scope" in g && t(16, i = g.$$scope);
  }, n.$$.update = () => {
    n.$$.dirty & /*dragging*/
    256 && w("drag", h);
  }, [
    s,
    f,
    a,
    r,
    c,
    d,
    _,
    m,
    h,
    p,
    y,
    q,
    u,
    l,
    z,
    F,
    i
  ];
}
class uf extends Rr {
  constructor(e) {
    super(), $r(this, e, ff, rf, ef, {
      value: 0,
      label: 1,
      show_label: 2,
      file_count: 3,
      file_types: 12,
      selectable: 4,
      root: 5,
      height: 6,
      i18n: 7
    });
  }
}
function _t(n) {
  let e = ["", "k", "M", "G", "T", "P", "E", "Z"], t = 0;
  for (; n > 1e3 && t < e.length - 1; )
    n /= 1e3, t++;
  let l = e[t];
  return (Number.isInteger(n) ? n : n.toFixed(1)) + l;
}
function Mt() {
}
function cf(n, e) {
  return n != n ? e == e : n !== e || n && typeof n == "object" || typeof n == "function";
}
const ji = typeof window < "u";
let Fl = ji ? () => window.performance.now() : () => Date.now(), Ni = ji ? (n) => requestAnimationFrame(n) : Mt;
const pt = /* @__PURE__ */ new Set();
function Fi(n) {
  pt.forEach((e) => {
    e.c(n) || (pt.delete(e), e.f());
  }), pt.size !== 0 && Ni(Fi);
}
function _f(n) {
  let e;
  return pt.size === 0 && Ni(Fi), {
    promise: new Promise((t) => {
      pt.add(e = { c: n, f: t });
    }),
    abort() {
      pt.delete(e);
    }
  };
}
const ft = [];
function df(n, e = Mt) {
  let t;
  const l = /* @__PURE__ */ new Set();
  function i(f) {
    if (cf(n, f) && (n = f, t)) {
      const a = !ft.length;
      for (const r of l)
        r[1](), ft.push(r, n);
      if (a) {
        for (let r = 0; r < ft.length; r += 2)
          ft[r][0](ft[r + 1]);
        ft.length = 0;
      }
    }
  }
  function o(f) {
    i(f(n));
  }
  function s(f, a = Mt) {
    const r = [f, a];
    return l.add(r), l.size === 1 && (t = e(i, o) || Mt), f(n), () => {
      l.delete(r), l.size === 0 && t && (t(), t = null);
    };
  }
  return { set: i, update: o, subscribe: s };
}
function Al(n) {
  return Object.prototype.toString.call(n) === "[object Date]";
}
function On(n, e, t, l) {
  if (typeof t == "number" || Al(t)) {
    const i = l - t, o = (t - e) / (n.dt || 1 / 60), s = n.opts.stiffness * i, f = n.opts.damping * o, a = (s - f) * n.inv_mass, r = (o + a) * n.dt;
    return Math.abs(r) < n.opts.precision && Math.abs(i) < n.opts.precision ? l : (n.settled = !1, Al(t) ? new Date(t.getTime() + r) : t + r);
  } else {
    if (Array.isArray(t))
      return t.map(
        (i, o) => On(n, e[o], t[o], l[o])
      );
    if (typeof t == "object") {
      const i = {};
      for (const o in t)
        i[o] = On(n, e[o], t[o], l[o]);
      return i;
    } else
      throw new Error(`Cannot spring ${typeof t} values`);
  }
}
function Ll(n, e = {}) {
  const t = df(n), { stiffness: l = 0.15, damping: i = 0.8, precision: o = 0.01 } = e;
  let s, f, a, r = n, u = n, c = 1, d = 0, _ = !1;
  function m(q, w = {}) {
    u = q;
    const p = a = {};
    return n == null || w.hard || y.stiffness >= 1 && y.damping >= 1 ? (_ = !0, s = Fl(), r = q, t.set(n = u), Promise.resolve()) : (w.soft && (d = 1 / ((w.soft === !0 ? 0.5 : +w.soft) * 60), c = 0), f || (s = Fl(), _ = !1, f = _f((h) => {
      if (_)
        return _ = !1, f = null, !1;
      c = Math.min(c + d, 1);
      const z = {
        inv_mass: c,
        opts: y,
        settled: !0,
        dt: (h - s) * 60 / 1e3
      }, F = On(z, r, n, u);
      return s = h, r = n, t.set(n = F), z.settled && (f = null), !z.settled;
    })), new Promise((h) => {
      f.promise.then(() => {
        p === a && h();
      });
    }));
  }
  const y = {
    set: m,
    update: (q, w) => m(q(u, n), w),
    subscribe: t.subscribe,
    stiffness: l,
    damping: i,
    precision: o
  };
  return y;
}
const {
  SvelteComponent: mf,
  append: qe,
  attr: O,
  component_subscribe: Bl,
  detach: gf,
  element: hf,
  init: pf,
  insert: bf,
  noop: Il,
  safe_not_equal: wf,
  set_style: It,
  svg_element: Se,
  toggle_class: Ol
} = window.__gradio__svelte__internal, { onMount: vf } = window.__gradio__svelte__internal;
function kf(n) {
  let e, t, l, i, o, s, f, a, r, u, c, d;
  return {
    c() {
      e = hf("div"), t = Se("svg"), l = Se("g"), i = Se("path"), o = Se("path"), s = Se("path"), f = Se("path"), a = Se("g"), r = Se("path"), u = Se("path"), c = Se("path"), d = Se("path"), O(i, "d", "M255.926 0.754768L509.702 139.936V221.027L255.926 81.8465V0.754768Z"), O(i, "fill", "#FF7C00"), O(i, "fill-opacity", "0.4"), O(i, "class", "svelte-43sxxs"), O(o, "d", "M509.69 139.936L254.981 279.641V361.255L509.69 221.55V139.936Z"), O(o, "fill", "#FF7C00"), O(o, "class", "svelte-43sxxs"), O(s, "d", "M0.250138 139.937L254.981 279.641V361.255L0.250138 221.55V139.937Z"), O(s, "fill", "#FF7C00"), O(s, "fill-opacity", "0.4"), O(s, "class", "svelte-43sxxs"), O(f, "d", "M255.923 0.232622L0.236328 139.936V221.55L255.923 81.8469V0.232622Z"), O(f, "fill", "#FF7C00"), O(f, "class", "svelte-43sxxs"), It(l, "transform", "translate(" + /*$top*/
      n[1][0] + "px, " + /*$top*/
      n[1][1] + "px)"), O(r, "d", "M255.926 141.5L509.702 280.681V361.773L255.926 222.592V141.5Z"), O(r, "fill", "#FF7C00"), O(r, "fill-opacity", "0.4"), O(r, "class", "svelte-43sxxs"), O(u, "d", "M509.69 280.679L254.981 420.384V501.998L509.69 362.293V280.679Z"), O(u, "fill", "#FF7C00"), O(u, "class", "svelte-43sxxs"), O(c, "d", "M0.250138 280.681L254.981 420.386V502L0.250138 362.295V280.681Z"), O(c, "fill", "#FF7C00"), O(c, "fill-opacity", "0.4"), O(c, "class", "svelte-43sxxs"), O(d, "d", "M255.923 140.977L0.236328 280.68V362.294L255.923 222.591V140.977Z"), O(d, "fill", "#FF7C00"), O(d, "class", "svelte-43sxxs"), It(a, "transform", "translate(" + /*$bottom*/
      n[2][0] + "px, " + /*$bottom*/
      n[2][1] + "px)"), O(t, "viewBox", "-1200 -1200 3000 3000"), O(t, "fill", "none"), O(t, "xmlns", "http://www.w3.org/2000/svg"), O(t, "class", "svelte-43sxxs"), O(e, "class", "svelte-43sxxs"), Ol(
        e,
        "margin",
        /*margin*/
        n[0]
      );
    },
    m(_, m) {
      bf(_, e, m), qe(e, t), qe(t, l), qe(l, i), qe(l, o), qe(l, s), qe(l, f), qe(t, a), qe(a, r), qe(a, u), qe(a, c), qe(a, d);
    },
    p(_, [m]) {
      m & /*$top*/
      2 && It(l, "transform", "translate(" + /*$top*/
      _[1][0] + "px, " + /*$top*/
      _[1][1] + "px)"), m & /*$bottom*/
      4 && It(a, "transform", "translate(" + /*$bottom*/
      _[2][0] + "px, " + /*$bottom*/
      _[2][1] + "px)"), m & /*margin*/
      1 && Ol(
        e,
        "margin",
        /*margin*/
        _[0]
      );
    },
    i: Il,
    o: Il,
    d(_) {
      _ && gf(e);
    }
  };
}
function yf(n, e, t) {
  let l, i;
  var o = this && this.__awaiter || function(_, m, y, q) {
    function w(p) {
      return p instanceof y ? p : new y(function(h) {
        h(p);
      });
    }
    return new (y || (y = Promise))(function(p, h) {
      function z(D) {
        try {
          g(q.next(D));
        } catch (T) {
          h(T);
        }
      }
      function F(D) {
        try {
          g(q.throw(D));
        } catch (T) {
          h(T);
        }
      }
      function g(D) {
        D.done ? p(D.value) : w(D.value).then(z, F);
      }
      g((q = q.apply(_, m || [])).next());
    });
  };
  let { margin: s = !0 } = e;
  const f = Ll([0, 0]);
  Bl(n, f, (_) => t(1, l = _));
  const a = Ll([0, 0]);
  Bl(n, a, (_) => t(2, i = _));
  let r;
  function u() {
    return o(this, void 0, void 0, function* () {
      yield Promise.all([f.set([125, 140]), a.set([-125, -140])]), yield Promise.all([f.set([-125, 140]), a.set([125, -140])]), yield Promise.all([f.set([-125, 0]), a.set([125, -0])]), yield Promise.all([f.set([125, 0]), a.set([-125, 0])]);
    });
  }
  function c() {
    return o(this, void 0, void 0, function* () {
      yield u(), r || c();
    });
  }
  function d() {
    return o(this, void 0, void 0, function* () {
      yield Promise.all([f.set([125, 0]), a.set([-125, 0])]), c();
    });
  }
  return vf(() => (d(), () => r = !0)), n.$$set = (_) => {
    "margin" in _ && t(0, s = _.margin);
  }, [s, l, i, f, a];
}
class qf extends mf {
  constructor(e) {
    super(), pf(this, e, yf, kf, wf, { margin: 0 });
  }
}
const {
  SvelteComponent: Sf,
  append: Qe,
  attr: De,
  binding_callbacks: Pl,
  check_outros: Ai,
  create_component: Cf,
  create_slot: zf,
  destroy_component: Df,
  destroy_each: Li,
  detach: j,
  element: Ie,
  empty: vt,
  ensure_array_like: Kt,
  get_all_dirty_from_scope: Ef,
  get_slot_changes: jf,
  group_outros: Bi,
  init: Nf,
  insert: N,
  mount_component: Ff,
  noop: Pn,
  safe_not_equal: Af,
  set_data: we,
  set_style: Te,
  space: Ee,
  text: X,
  toggle_class: pe,
  transition_in: bt,
  transition_out: wt,
  update_slot_base: Lf
} = window.__gradio__svelte__internal, { tick: Bf } = window.__gradio__svelte__internal, { onDestroy: If } = window.__gradio__svelte__internal, Of = (n) => ({}), Ul = (n) => ({});
function Ml(n, e, t) {
  const l = n.slice();
  return l[39] = e[t], l[41] = t, l;
}
function Tl(n, e, t) {
  const l = n.slice();
  return l[39] = e[t], l;
}
function Pf(n) {
  let e, t = (
    /*i18n*/
    n[1]("common.error") + ""
  ), l, i, o;
  const s = (
    /*#slots*/
    n[29].error
  ), f = zf(
    s,
    n,
    /*$$scope*/
    n[28],
    Ul
  );
  return {
    c() {
      e = Ie("span"), l = X(t), i = Ee(), f && f.c(), De(e, "class", "error svelte-1txqlrd");
    },
    m(a, r) {
      N(a, e, r), Qe(e, l), N(a, i, r), f && f.m(a, r), o = !0;
    },
    p(a, r) {
      (!o || r[0] & /*i18n*/
      2) && t !== (t = /*i18n*/
      a[1]("common.error") + "") && we(l, t), f && f.p && (!o || r[0] & /*$$scope*/
      268435456) && Lf(
        f,
        s,
        a,
        /*$$scope*/
        a[28],
        o ? jf(
          s,
          /*$$scope*/
          a[28],
          r,
          Of
        ) : Ef(
          /*$$scope*/
          a[28]
        ),
        Ul
      );
    },
    i(a) {
      o || (bt(f, a), o = !0);
    },
    o(a) {
      wt(f, a), o = !1;
    },
    d(a) {
      a && (j(e), j(i)), f && f.d(a);
    }
  };
}
function Uf(n) {
  let e, t, l, i, o, s, f, a, r, u = (
    /*variant*/
    n[8] === "default" && /*show_eta_bar*/
    n[18] && /*show_progress*/
    n[6] === "full" && Vl(n)
  );
  function c(h, z) {
    if (
      /*progress*/
      h[7]
    ) return Vf;
    if (
      /*queue_position*/
      h[2] !== null && /*queue_size*/
      h[3] !== void 0 && /*queue_position*/
      h[2] >= 0
    ) return Tf;
    if (
      /*queue_position*/
      h[2] === 0
    ) return Mf;
  }
  let d = c(n), _ = d && d(n), m = (
    /*timer*/
    n[5] && Jl(n)
  );
  const y = [Gf, Jf], q = [];
  function w(h, z) {
    return (
      /*last_progress_level*/
      h[15] != null ? 0 : (
        /*show_progress*/
        h[6] === "full" ? 1 : -1
      )
    );
  }
  ~(o = w(n)) && (s = q[o] = y[o](n));
  let p = !/*timer*/
  n[5] && Ql(n);
  return {
    c() {
      u && u.c(), e = Ee(), t = Ie("div"), _ && _.c(), l = Ee(), m && m.c(), i = Ee(), s && s.c(), f = Ee(), p && p.c(), a = vt(), De(t, "class", "progress-text svelte-1txqlrd"), pe(
        t,
        "meta-text-center",
        /*variant*/
        n[8] === "center"
      ), pe(
        t,
        "meta-text",
        /*variant*/
        n[8] === "default"
      );
    },
    m(h, z) {
      u && u.m(h, z), N(h, e, z), N(h, t, z), _ && _.m(t, null), Qe(t, l), m && m.m(t, null), N(h, i, z), ~o && q[o].m(h, z), N(h, f, z), p && p.m(h, z), N(h, a, z), r = !0;
    },
    p(h, z) {
      /*variant*/
      h[8] === "default" && /*show_eta_bar*/
      h[18] && /*show_progress*/
      h[6] === "full" ? u ? u.p(h, z) : (u = Vl(h), u.c(), u.m(e.parentNode, e)) : u && (u.d(1), u = null), d === (d = c(h)) && _ ? _.p(h, z) : (_ && _.d(1), _ = d && d(h), _ && (_.c(), _.m(t, l))), /*timer*/
      h[5] ? m ? m.p(h, z) : (m = Jl(h), m.c(), m.m(t, null)) : m && (m.d(1), m = null), (!r || z[0] & /*variant*/
      256) && pe(
        t,
        "meta-text-center",
        /*variant*/
        h[8] === "center"
      ), (!r || z[0] & /*variant*/
      256) && pe(
        t,
        "meta-text",
        /*variant*/
        h[8] === "default"
      );
      let F = o;
      o = w(h), o === F ? ~o && q[o].p(h, z) : (s && (Bi(), wt(q[F], 1, 1, () => {
        q[F] = null;
      }), Ai()), ~o ? (s = q[o], s ? s.p(h, z) : (s = q[o] = y[o](h), s.c()), bt(s, 1), s.m(f.parentNode, f)) : s = null), /*timer*/
      h[5] ? p && (p.d(1), p = null) : p ? p.p(h, z) : (p = Ql(h), p.c(), p.m(a.parentNode, a));
    },
    i(h) {
      r || (bt(s), r = !0);
    },
    o(h) {
      wt(s), r = !1;
    },
    d(h) {
      h && (j(e), j(t), j(i), j(f), j(a)), u && u.d(h), _ && _.d(), m && m.d(), ~o && q[o].d(h), p && p.d(h);
    }
  };
}
function Vl(n) {
  let e, t = `translateX(${/*eta_level*/
  (n[17] || 0) * 100 - 100}%)`;
  return {
    c() {
      e = Ie("div"), De(e, "class", "eta-bar svelte-1txqlrd"), Te(e, "transform", t);
    },
    m(l, i) {
      N(l, e, i);
    },
    p(l, i) {
      i[0] & /*eta_level*/
      131072 && t !== (t = `translateX(${/*eta_level*/
      (l[17] || 0) * 100 - 100}%)`) && Te(e, "transform", t);
    },
    d(l) {
      l && j(e);
    }
  };
}
function Mf(n) {
  let e;
  return {
    c() {
      e = X("processing |");
    },
    m(t, l) {
      N(t, e, l);
    },
    p: Pn,
    d(t) {
      t && j(e);
    }
  };
}
function Tf(n) {
  let e, t = (
    /*queue_position*/
    n[2] + 1 + ""
  ), l, i, o, s;
  return {
    c() {
      e = X("queue: "), l = X(t), i = X("/"), o = X(
        /*queue_size*/
        n[3]
      ), s = X(" |");
    },
    m(f, a) {
      N(f, e, a), N(f, l, a), N(f, i, a), N(f, o, a), N(f, s, a);
    },
    p(f, a) {
      a[0] & /*queue_position*/
      4 && t !== (t = /*queue_position*/
      f[2] + 1 + "") && we(l, t), a[0] & /*queue_size*/
      8 && we(
        o,
        /*queue_size*/
        f[3]
      );
    },
    d(f) {
      f && (j(e), j(l), j(i), j(o), j(s));
    }
  };
}
function Vf(n) {
  let e, t = Kt(
    /*progress*/
    n[7]
  ), l = [];
  for (let i = 0; i < t.length; i += 1)
    l[i] = Wl(Tl(n, t, i));
  return {
    c() {
      for (let i = 0; i < l.length; i += 1)
        l[i].c();
      e = vt();
    },
    m(i, o) {
      for (let s = 0; s < l.length; s += 1)
        l[s] && l[s].m(i, o);
      N(i, e, o);
    },
    p(i, o) {
      if (o[0] & /*progress*/
      128) {
        t = Kt(
          /*progress*/
          i[7]
        );
        let s;
        for (s = 0; s < t.length; s += 1) {
          const f = Tl(i, t, s);
          l[s] ? l[s].p(f, o) : (l[s] = Wl(f), l[s].c(), l[s].m(e.parentNode, e));
        }
        for (; s < l.length; s += 1)
          l[s].d(1);
        l.length = t.length;
      }
    },
    d(i) {
      i && j(e), Li(l, i);
    }
  };
}
function Rl(n) {
  let e, t = (
    /*p*/
    n[39].unit + ""
  ), l, i, o = " ", s;
  function f(u, c) {
    return (
      /*p*/
      u[39].length != null ? Wf : Rf
    );
  }
  let a = f(n), r = a(n);
  return {
    c() {
      r.c(), e = Ee(), l = X(t), i = X(" | "), s = X(o);
    },
    m(u, c) {
      r.m(u, c), N(u, e, c), N(u, l, c), N(u, i, c), N(u, s, c);
    },
    p(u, c) {
      a === (a = f(u)) && r ? r.p(u, c) : (r.d(1), r = a(u), r && (r.c(), r.m(e.parentNode, e))), c[0] & /*progress*/
      128 && t !== (t = /*p*/
      u[39].unit + "") && we(l, t);
    },
    d(u) {
      u && (j(e), j(l), j(i), j(s)), r.d(u);
    }
  };
}
function Rf(n) {
  let e = _t(
    /*p*/
    n[39].index || 0
  ) + "", t;
  return {
    c() {
      t = X(e);
    },
    m(l, i) {
      N(l, t, i);
    },
    p(l, i) {
      i[0] & /*progress*/
      128 && e !== (e = _t(
        /*p*/
        l[39].index || 0
      ) + "") && we(t, e);
    },
    d(l) {
      l && j(t);
    }
  };
}
function Wf(n) {
  let e = _t(
    /*p*/
    n[39].index || 0
  ) + "", t, l, i = _t(
    /*p*/
    n[39].length
  ) + "", o;
  return {
    c() {
      t = X(e), l = X("/"), o = X(i);
    },
    m(s, f) {
      N(s, t, f), N(s, l, f), N(s, o, f);
    },
    p(s, f) {
      f[0] & /*progress*/
      128 && e !== (e = _t(
        /*p*/
        s[39].index || 0
      ) + "") && we(t, e), f[0] & /*progress*/
      128 && i !== (i = _t(
        /*p*/
        s[39].length
      ) + "") && we(o, i);
    },
    d(s) {
      s && (j(t), j(l), j(o));
    }
  };
}
function Wl(n) {
  let e, t = (
    /*p*/
    n[39].index != null && Rl(n)
  );
  return {
    c() {
      t && t.c(), e = vt();
    },
    m(l, i) {
      t && t.m(l, i), N(l, e, i);
    },
    p(l, i) {
      /*p*/
      l[39].index != null ? t ? t.p(l, i) : (t = Rl(l), t.c(), t.m(e.parentNode, e)) : t && (t.d(1), t = null);
    },
    d(l) {
      l && j(e), t && t.d(l);
    }
  };
}
function Jl(n) {
  let e, t = (
    /*eta*/
    n[0] ? `/${/*formatted_eta*/
    n[19]}` : ""
  ), l, i;
  return {
    c() {
      e = X(
        /*formatted_timer*/
        n[20]
      ), l = X(t), i = X("s");
    },
    m(o, s) {
      N(o, e, s), N(o, l, s), N(o, i, s);
    },
    p(o, s) {
      s[0] & /*formatted_timer*/
      1048576 && we(
        e,
        /*formatted_timer*/
        o[20]
      ), s[0] & /*eta, formatted_eta*/
      524289 && t !== (t = /*eta*/
      o[0] ? `/${/*formatted_eta*/
      o[19]}` : "") && we(l, t);
    },
    d(o) {
      o && (j(e), j(l), j(i));
    }
  };
}
function Jf(n) {
  let e, t;
  return e = new qf({
    props: { margin: (
      /*variant*/
      n[8] === "default"
    ) }
  }), {
    c() {
      Cf(e.$$.fragment);
    },
    m(l, i) {
      Ff(e, l, i), t = !0;
    },
    p(l, i) {
      const o = {};
      i[0] & /*variant*/
      256 && (o.margin = /*variant*/
      l[8] === "default"), e.$set(o);
    },
    i(l) {
      t || (bt(e.$$.fragment, l), t = !0);
    },
    o(l) {
      wt(e.$$.fragment, l), t = !1;
    },
    d(l) {
      Df(e, l);
    }
  };
}
function Gf(n) {
  let e, t, l, i, o, s = `${/*last_progress_level*/
  n[15] * 100}%`, f = (
    /*progress*/
    n[7] != null && Gl(n)
  );
  return {
    c() {
      e = Ie("div"), t = Ie("div"), f && f.c(), l = Ee(), i = Ie("div"), o = Ie("div"), De(t, "class", "progress-level-inner svelte-1txqlrd"), De(o, "class", "progress-bar svelte-1txqlrd"), Te(o, "width", s), De(i, "class", "progress-bar-wrap svelte-1txqlrd"), De(e, "class", "progress-level svelte-1txqlrd");
    },
    m(a, r) {
      N(a, e, r), Qe(e, t), f && f.m(t, null), Qe(e, l), Qe(e, i), Qe(i, o), n[30](o);
    },
    p(a, r) {
      /*progress*/
      a[7] != null ? f ? f.p(a, r) : (f = Gl(a), f.c(), f.m(t, null)) : f && (f.d(1), f = null), r[0] & /*last_progress_level*/
      32768 && s !== (s = `${/*last_progress_level*/
      a[15] * 100}%`) && Te(o, "width", s);
    },
    i: Pn,
    o: Pn,
    d(a) {
      a && j(e), f && f.d(), n[30](null);
    }
  };
}
function Gl(n) {
  let e, t = Kt(
    /*progress*/
    n[7]
  ), l = [];
  for (let i = 0; i < t.length; i += 1)
    l[i] = Yl(Ml(n, t, i));
  return {
    c() {
      for (let i = 0; i < l.length; i += 1)
        l[i].c();
      e = vt();
    },
    m(i, o) {
      for (let s = 0; s < l.length; s += 1)
        l[s] && l[s].m(i, o);
      N(i, e, o);
    },
    p(i, o) {
      if (o[0] & /*progress_level, progress*/
      16512) {
        t = Kt(
          /*progress*/
          i[7]
        );
        let s;
        for (s = 0; s < t.length; s += 1) {
          const f = Ml(i, t, s);
          l[s] ? l[s].p(f, o) : (l[s] = Yl(f), l[s].c(), l[s].m(e.parentNode, e));
        }
        for (; s < l.length; s += 1)
          l[s].d(1);
        l.length = t.length;
      }
    },
    d(i) {
      i && j(e), Li(l, i);
    }
  };
}
function Zl(n) {
  let e, t, l, i, o = (
    /*i*/
    n[41] !== 0 && Zf()
  ), s = (
    /*p*/
    n[39].desc != null && Hl(n)
  ), f = (
    /*p*/
    n[39].desc != null && /*progress_level*/
    n[14] && /*progress_level*/
    n[14][
      /*i*/
      n[41]
    ] != null && Kl()
  ), a = (
    /*progress_level*/
    n[14] != null && Xl(n)
  );
  return {
    c() {
      o && o.c(), e = Ee(), s && s.c(), t = Ee(), f && f.c(), l = Ee(), a && a.c(), i = vt();
    },
    m(r, u) {
      o && o.m(r, u), N(r, e, u), s && s.m(r, u), N(r, t, u), f && f.m(r, u), N(r, l, u), a && a.m(r, u), N(r, i, u);
    },
    p(r, u) {
      /*p*/
      r[39].desc != null ? s ? s.p(r, u) : (s = Hl(r), s.c(), s.m(t.parentNode, t)) : s && (s.d(1), s = null), /*p*/
      r[39].desc != null && /*progress_level*/
      r[14] && /*progress_level*/
      r[14][
        /*i*/
        r[41]
      ] != null ? f || (f = Kl(), f.c(), f.m(l.parentNode, l)) : f && (f.d(1), f = null), /*progress_level*/
      r[14] != null ? a ? a.p(r, u) : (a = Xl(r), a.c(), a.m(i.parentNode, i)) : a && (a.d(1), a = null);
    },
    d(r) {
      r && (j(e), j(t), j(l), j(i)), o && o.d(r), s && s.d(r), f && f.d(r), a && a.d(r);
    }
  };
}
function Zf(n) {
  let e;
  return {
    c() {
      e = X(" /");
    },
    m(t, l) {
      N(t, e, l);
    },
    d(t) {
      t && j(e);
    }
  };
}
function Hl(n) {
  let e = (
    /*p*/
    n[39].desc + ""
  ), t;
  return {
    c() {
      t = X(e);
    },
    m(l, i) {
      N(l, t, i);
    },
    p(l, i) {
      i[0] & /*progress*/
      128 && e !== (e = /*p*/
      l[39].desc + "") && we(t, e);
    },
    d(l) {
      l && j(t);
    }
  };
}
function Kl(n) {
  let e;
  return {
    c() {
      e = X("-");
    },
    m(t, l) {
      N(t, e, l);
    },
    d(t) {
      t && j(e);
    }
  };
}
function Xl(n) {
  let e = (100 * /*progress_level*/
  (n[14][
    /*i*/
    n[41]
  ] || 0)).toFixed(1) + "", t, l;
  return {
    c() {
      t = X(e), l = X("%");
    },
    m(i, o) {
      N(i, t, o), N(i, l, o);
    },
    p(i, o) {
      o[0] & /*progress_level*/
      16384 && e !== (e = (100 * /*progress_level*/
      (i[14][
        /*i*/
        i[41]
      ] || 0)).toFixed(1) + "") && we(t, e);
    },
    d(i) {
      i && (j(t), j(l));
    }
  };
}
function Yl(n) {
  let e, t = (
    /*p*/
    (n[39].desc != null || /*progress_level*/
    n[14] && /*progress_level*/
    n[14][
      /*i*/
      n[41]
    ] != null) && Zl(n)
  );
  return {
    c() {
      t && t.c(), e = vt();
    },
    m(l, i) {
      t && t.m(l, i), N(l, e, i);
    },
    p(l, i) {
      /*p*/
      l[39].desc != null || /*progress_level*/
      l[14] && /*progress_level*/
      l[14][
        /*i*/
        l[41]
      ] != null ? t ? t.p(l, i) : (t = Zl(l), t.c(), t.m(e.parentNode, e)) : t && (t.d(1), t = null);
    },
    d(l) {
      l && j(e), t && t.d(l);
    }
  };
}
function Ql(n) {
  let e, t;
  return {
    c() {
      e = Ie("p"), t = X(
        /*loading_text*/
        n[9]
      ), De(e, "class", "loading svelte-1txqlrd");
    },
    m(l, i) {
      N(l, e, i), Qe(e, t);
    },
    p(l, i) {
      i[0] & /*loading_text*/
      512 && we(
        t,
        /*loading_text*/
        l[9]
      );
    },
    d(l) {
      l && j(e);
    }
  };
}
function Hf(n) {
  let e, t, l, i, o;
  const s = [Uf, Pf], f = [];
  function a(r, u) {
    return (
      /*status*/
      r[4] === "pending" ? 0 : (
        /*status*/
        r[4] === "error" ? 1 : -1
      )
    );
  }
  return ~(t = a(n)) && (l = f[t] = s[t](n)), {
    c() {
      e = Ie("div"), l && l.c(), De(e, "class", i = "wrap " + /*variant*/
      n[8] + " " + /*show_progress*/
      n[6] + " svelte-1txqlrd"), pe(e, "hide", !/*status*/
      n[4] || /*status*/
      n[4] === "complete" || /*show_progress*/
      n[6] === "hidden"), pe(
        e,
        "translucent",
        /*variant*/
        n[8] === "center" && /*status*/
        (n[4] === "pending" || /*status*/
        n[4] === "error") || /*translucent*/
        n[11] || /*show_progress*/
        n[6] === "minimal"
      ), pe(
        e,
        "generating",
        /*status*/
        n[4] === "generating"
      ), pe(
        e,
        "border",
        /*border*/
        n[12]
      ), Te(
        e,
        "position",
        /*absolute*/
        n[10] ? "absolute" : "static"
      ), Te(
        e,
        "padding",
        /*absolute*/
        n[10] ? "0" : "var(--size-8) 0"
      );
    },
    m(r, u) {
      N(r, e, u), ~t && f[t].m(e, null), n[31](e), o = !0;
    },
    p(r, u) {
      let c = t;
      t = a(r), t === c ? ~t && f[t].p(r, u) : (l && (Bi(), wt(f[c], 1, 1, () => {
        f[c] = null;
      }), Ai()), ~t ? (l = f[t], l ? l.p(r, u) : (l = f[t] = s[t](r), l.c()), bt(l, 1), l.m(e, null)) : l = null), (!o || u[0] & /*variant, show_progress*/
      320 && i !== (i = "wrap " + /*variant*/
      r[8] + " " + /*show_progress*/
      r[6] + " svelte-1txqlrd")) && De(e, "class", i), (!o || u[0] & /*variant, show_progress, status, show_progress*/
      336) && pe(e, "hide", !/*status*/
      r[4] || /*status*/
      r[4] === "complete" || /*show_progress*/
      r[6] === "hidden"), (!o || u[0] & /*variant, show_progress, variant, status, translucent, show_progress*/
      2384) && pe(
        e,
        "translucent",
        /*variant*/
        r[8] === "center" && /*status*/
        (r[4] === "pending" || /*status*/
        r[4] === "error") || /*translucent*/
        r[11] || /*show_progress*/
        r[6] === "minimal"
      ), (!o || u[0] & /*variant, show_progress, status*/
      336) && pe(
        e,
        "generating",
        /*status*/
        r[4] === "generating"
      ), (!o || u[0] & /*variant, show_progress, border*/
      4416) && pe(
        e,
        "border",
        /*border*/
        r[12]
      ), u[0] & /*absolute*/
      1024 && Te(
        e,
        "position",
        /*absolute*/
        r[10] ? "absolute" : "static"
      ), u[0] & /*absolute*/
      1024 && Te(
        e,
        "padding",
        /*absolute*/
        r[10] ? "0" : "var(--size-8) 0"
      );
    },
    i(r) {
      o || (bt(l), o = !0);
    },
    o(r) {
      wt(l), o = !1;
    },
    d(r) {
      r && j(e), ~t && f[t].d(), n[31](null);
    }
  };
}
var Kf = function(n, e, t, l) {
  function i(o) {
    return o instanceof t ? o : new t(function(s) {
      s(o);
    });
  }
  return new (t || (t = Promise))(function(o, s) {
    function f(u) {
      try {
        r(l.next(u));
      } catch (c) {
        s(c);
      }
    }
    function a(u) {
      try {
        r(l.throw(u));
      } catch (c) {
        s(c);
      }
    }
    function r(u) {
      u.done ? o(u.value) : i(u.value).then(f, a);
    }
    r((l = l.apply(n, e || [])).next());
  });
};
let Ot = [], kn = !1;
function Xf(n) {
  return Kf(this, arguments, void 0, function* (e, t = !0) {
    if (!(window.__gradio_mode__ === "website" || window.__gradio_mode__ !== "app" && t !== !0)) {
      if (Ot.push(e), !kn) kn = !0;
      else return;
      yield Bf(), requestAnimationFrame(() => {
        let l = [0, 0];
        for (let i = 0; i < Ot.length; i++) {
          const s = Ot[i].getBoundingClientRect();
          (i === 0 || s.top + window.scrollY <= l[0]) && (l[0] = s.top + window.scrollY, l[1] = i);
        }
        window.scrollTo({ top: l[0] - 20, behavior: "smooth" }), kn = !1, Ot = [];
      });
    }
  });
}
function Yf(n, e, t) {
  let l, { $$slots: i = {}, $$scope: o } = e;
  this && this.__awaiter;
  let { i18n: s } = e, { eta: f = null } = e, { queue_position: a } = e, { queue_size: r } = e, { status: u } = e, { scroll_to_output: c = !1 } = e, { timer: d = !0 } = e, { show_progress: _ = "full" } = e, { message: m = null } = e, { progress: y = null } = e, { variant: q = "default" } = e, { loading_text: w = "Loading..." } = e, { absolute: p = !0 } = e, { translucent: h = !1 } = e, { border: z = !1 } = e, { autoscroll: F } = e, g, D = !1, T = 0, S = 0, B = null, I = null, W = 0, G = null, C, te = null, ae = !0;
  const je = () => {
    t(0, f = t(26, B = t(19, Ne = null))), t(24, T = performance.now()), t(25, S = 0), D = !0, Oe();
  };
  function Oe() {
    requestAnimationFrame(() => {
      t(25, S = (performance.now() - T) / 1e3), D && Oe();
    });
  }
  function ot() {
    t(25, S = 0), t(0, f = t(26, B = t(19, Ne = null))), D && (D = !1);
  }
  If(() => {
    D && ot();
  });
  let Ne = null;
  function L(b) {
    Pl[b ? "unshift" : "push"](() => {
      te = b, t(16, te), t(7, y), t(14, G), t(15, C);
    });
  }
  function v(b) {
    Pl[b ? "unshift" : "push"](() => {
      g = b, t(13, g);
    });
  }
  return n.$$set = (b) => {
    "i18n" in b && t(1, s = b.i18n), "eta" in b && t(0, f = b.eta), "queue_position" in b && t(2, a = b.queue_position), "queue_size" in b && t(3, r = b.queue_size), "status" in b && t(4, u = b.status), "scroll_to_output" in b && t(21, c = b.scroll_to_output), "timer" in b && t(5, d = b.timer), "show_progress" in b && t(6, _ = b.show_progress), "message" in b && t(22, m = b.message), "progress" in b && t(7, y = b.progress), "variant" in b && t(8, q = b.variant), "loading_text" in b && t(9, w = b.loading_text), "absolute" in b && t(10, p = b.absolute), "translucent" in b && t(11, h = b.translucent), "border" in b && t(12, z = b.border), "autoscroll" in b && t(23, F = b.autoscroll), "$$scope" in b && t(28, o = b.$$scope);
  }, n.$$.update = () => {
    n.$$.dirty[0] & /*eta, old_eta, timer_start, eta_from_start*/
    218103809 && (f === null && t(0, f = B), f != null && B !== f && (t(27, I = (performance.now() - T) / 1e3 + f), t(19, Ne = I.toFixed(1)), t(26, B = f))), n.$$.dirty[0] & /*eta_from_start, timer_diff*/
    167772160 && t(17, W = I === null || I <= 0 || !S ? null : Math.min(S / I, 1)), n.$$.dirty[0] & /*progress*/
    128 && y != null && t(18, ae = !1), n.$$.dirty[0] & /*progress, progress_level, progress_bar, last_progress_level*/
    114816 && (y != null ? t(14, G = y.map((b) => {
      if (b.index != null && b.length != null)
        return b.index / b.length;
      if (b.progress != null)
        return b.progress;
    })) : t(14, G = null), G ? (t(15, C = G[G.length - 1]), te && (C === 0 ? t(16, te.style.transition = "0", te) : t(16, te.style.transition = "150ms", te))) : t(15, C = void 0)), n.$$.dirty[0] & /*status*/
    16 && (u === "pending" ? je() : ot()), n.$$.dirty[0] & /*el, scroll_to_output, status, autoscroll*/
    10493968 && g && c && (u === "pending" || u === "complete") && Xf(g, F), n.$$.dirty[0] & /*status, message*/
    4194320, n.$$.dirty[0] & /*timer_diff*/
    33554432 && t(20, l = S.toFixed(1));
  }, [
    f,
    s,
    a,
    r,
    u,
    d,
    _,
    y,
    q,
    w,
    p,
    h,
    z,
    g,
    G,
    C,
    te,
    W,
    ae,
    Ne,
    l,
    c,
    m,
    F,
    T,
    S,
    B,
    I,
    o,
    i,
    L,
    v
  ];
}
class Qf extends Sf {
  constructor(e) {
    super(), Nf(
      this,
      e,
      Yf,
      Hf,
      Af,
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
  SvelteComponent: xf,
  append: $f,
  attr: eu,
  detach: tu,
  element: nu,
  init: lu,
  insert: iu,
  noop: xl,
  safe_not_equal: ou,
  set_data: su,
  text: au,
  toggle_class: ut
} = window.__gradio__svelte__internal;
function ru(n) {
  let e, t = (Array.isArray(
    /*value*/
    n[0]
  ) ? (
    /*value*/
    n[0].join(", ")
  ) : (
    /*value*/
    n[0]
  )) + "", l;
  return {
    c() {
      e = nu("div"), l = au(t), eu(e, "class", "svelte-1hgn91n"), ut(
        e,
        "table",
        /*type*/
        n[1] === "table"
      ), ut(
        e,
        "gallery",
        /*type*/
        n[1] === "gallery"
      ), ut(
        e,
        "selected",
        /*selected*/
        n[2]
      );
    },
    m(i, o) {
      iu(i, e, o), $f(e, l);
    },
    p(i, [o]) {
      o & /*value*/
      1 && t !== (t = (Array.isArray(
        /*value*/
        i[0]
      ) ? (
        /*value*/
        i[0].join(", ")
      ) : (
        /*value*/
        i[0]
      )) + "") && su(l, t), o & /*type*/
      2 && ut(
        e,
        "table",
        /*type*/
        i[1] === "table"
      ), o & /*type*/
      2 && ut(
        e,
        "gallery",
        /*type*/
        i[1] === "gallery"
      ), o & /*selected*/
      4 && ut(
        e,
        "selected",
        /*selected*/
        i[2]
      );
    },
    i: xl,
    o: xl,
    d(i) {
      i && tu(e);
    }
  };
}
function fu(n, e, t) {
  let { value: l } = e, { type: i } = e, { selected: o = !1 } = e;
  return n.$$set = (s) => {
    "value" in s && t(0, l = s.value), "type" in s && t(1, i = s.type), "selected" in s && t(2, o = s.selected);
  }, [l, i, o];
}
class Au extends xf {
  constructor(e) {
    super(), lu(this, e, fu, ru, ou, { value: 0, type: 1, selected: 2 });
  }
}
const {
  SvelteComponent: uu,
  assign: cu,
  check_outros: _u,
  create_component: St,
  destroy_component: Ct,
  detach: $l,
  empty: du,
  flush: $,
  get_spread_object: mu,
  get_spread_update: gu,
  group_outros: hu,
  init: pu,
  insert: ei,
  mount_component: zt,
  safe_not_equal: bu,
  space: wu,
  transition_in: nt,
  transition_out: lt
} = window.__gradio__svelte__internal;
function vu(n) {
  let e, t;
  return e = new uf({
    props: {
      label: (
        /*label*/
        n[6]
      ),
      show_label: (
        /*show_label*/
        n[7]
      ),
      value: (
        /*_value*/
        n[17]
      ),
      file_count: (
        /*file_count*/
        n[15]
      ),
      file_types: (
        /*file_types*/
        n[16]
      ),
      selectable: (
        /*_selectable*/
        n[9]
      ),
      root: (
        /*root*/
        n[5]
      ),
      height: (
        /*height*/
        n[8]
      ),
      i18n: (
        /*gradio*/
        n[14].i18n
      ),
      $$slots: { default: [yu] },
      $$scope: { ctx: n }
    }
  }), e.$on(
    "change",
    /*change_handler*/
    n[22]
  ), e.$on(
    "drag",
    /*drag_handler*/
    n[23]
  ), e.$on(
    "clear",
    /*clear_handler*/
    n[24]
  ), e.$on(
    "select",
    /*select_handler_1*/
    n[25]
  ), e.$on(
    "upload",
    /*upload_handler*/
    n[26]
  ), {
    c() {
      St(e.$$.fragment);
    },
    m(l, i) {
      zt(e, l, i), t = !0;
    },
    p(l, i) {
      const o = {};
      i & /*label*/
      64 && (o.label = /*label*/
      l[6]), i & /*show_label*/
      128 && (o.show_label = /*show_label*/
      l[7]), i & /*_value*/
      131072 && (o.value = /*_value*/
      l[17]), i & /*file_count*/
      32768 && (o.file_count = /*file_count*/
      l[15]), i & /*file_types*/
      65536 && (o.file_types = /*file_types*/
      l[16]), i & /*_selectable*/
      512 && (o.selectable = /*_selectable*/
      l[9]), i & /*root*/
      32 && (o.root = /*root*/
      l[5]), i & /*height*/
      256 && (o.height = /*height*/
      l[8]), i & /*gradio*/
      16384 && (o.i18n = /*gradio*/
      l[14].i18n), i & /*$$scope, gradio*/
      134234112 && (o.$$scope = { dirty: i, ctx: l }), e.$set(o);
    },
    i(l) {
      t || (nt(e.$$.fragment, l), t = !0);
    },
    o(l) {
      lt(e.$$.fragment, l), t = !1;
    },
    d(l) {
      Ct(e, l);
    }
  };
}
function ku(n) {
  let e, t;
  return e = new Da({
    props: {
      selectable: (
        /*_selectable*/
        n[9]
      ),
      value: (
        /*_value*/
        n[17]
      ),
      label: (
        /*label*/
        n[6]
      ),
      show_label: (
        /*show_label*/
        n[7]
      ),
      height: (
        /*height*/
        n[8]
      ),
      i18n: (
        /*gradio*/
        n[14].i18n
      )
    }
  }), e.$on(
    "select",
    /*select_handler*/
    n[21]
  ), {
    c() {
      St(e.$$.fragment);
    },
    m(l, i) {
      zt(e, l, i), t = !0;
    },
    p(l, i) {
      const o = {};
      i & /*_selectable*/
      512 && (o.selectable = /*_selectable*/
      l[9]), i & /*_value*/
      131072 && (o.value = /*_value*/
      l[17]), i & /*label*/
      64 && (o.label = /*label*/
      l[6]), i & /*show_label*/
      128 && (o.show_label = /*show_label*/
      l[7]), i & /*height*/
      256 && (o.height = /*height*/
      l[8]), i & /*gradio*/
      16384 && (o.i18n = /*gradio*/
      l[14].i18n), e.$set(o);
    },
    i(l) {
      t || (nt(e.$$.fragment, l), t = !0);
    },
    o(l) {
      lt(e.$$.fragment, l), t = !1;
    },
    d(l) {
      Ct(e, l);
    }
  };
}
function yu(n) {
  let e, t;
  return e = new ps({
    props: {
      i18n: (
        /*gradio*/
        n[14].i18n
      ),
      type: "file"
    }
  }), {
    c() {
      St(e.$$.fragment);
    },
    m(l, i) {
      zt(e, l, i), t = !0;
    },
    p(l, i) {
      const o = {};
      i & /*gradio*/
      16384 && (o.i18n = /*gradio*/
      l[14].i18n), e.$set(o);
    },
    i(l) {
      t || (nt(e.$$.fragment, l), t = !0);
    },
    o(l) {
      lt(e.$$.fragment, l), t = !1;
    },
    d(l) {
      Ct(e, l);
    }
  };
}
function qu(n) {
  let e, t, l, i, o, s;
  const f = [
    {
      autoscroll: (
        /*gradio*/
        n[14].autoscroll
      )
    },
    { i18n: (
      /*gradio*/
      n[14].i18n
    ) },
    /*loading_status*/
    n[10],
    {
      status: (
        /*loading_status*/
        n[10]?.status || "complete"
      )
    }
  ];
  let a = {};
  for (let d = 0; d < f.length; d += 1)
    a = cu(a, f[d]);
  e = new Qf({ props: a });
  const r = [ku, vu], u = [];
  function c(d, _) {
    return (
      /*interactive*/
      d[4] ? 1 : 0
    );
  }
  return l = c(n), i = u[l] = r[l](n), {
    c() {
      St(e.$$.fragment), t = wu(), i.c(), o = du();
    },
    m(d, _) {
      zt(e, d, _), ei(d, t, _), u[l].m(d, _), ei(d, o, _), s = !0;
    },
    p(d, _) {
      const m = _ & /*gradio, loading_status, pending_upload*/
      17408 ? gu(f, [
        _ & /*gradio*/
        16384 && {
          autoscroll: (
            /*gradio*/
            d[14].autoscroll
          )
        },
        _ & /*gradio*/
        16384 && { i18n: (
          /*gradio*/
          d[14].i18n
        ) },
        _ & /*loading_status*/
        1024 && mu(
          /*loading_status*/
          d[10]
        ),
        _ & /*pending_upload, loading_status*/
        1024 && {
          status: (
            /*loading_status*/
            d[10]?.status || "complete"
          )
        }
      ]) : {};
      e.$set(m);
      let y = l;
      l = c(d), l === y ? u[l].p(d, _) : (hu(), lt(u[y], 1, 1, () => {
        u[y] = null;
      }), _u(), i = u[l], i ? i.p(d, _) : (i = u[l] = r[l](d), i.c()), nt(i, 1), i.m(o.parentNode, o));
    },
    i(d) {
      s || (nt(e.$$.fragment, d), nt(i), s = !0);
    },
    o(d) {
      lt(e.$$.fragment, d), lt(i), s = !1;
    },
    d(d) {
      d && ($l(t), $l(o)), Ct(e, d), u[l].d(d);
    }
  };
}
function Su(n) {
  let e, t;
  return e = new Qi({
    props: {
      visible: (
        /*visible*/
        n[3]
      ),
      variant: (
        /*value*/
        n[0] === null ? "dashed" : "solid"
      ),
      border_mode: (
        /*dragging*/
        n[18] ? "focus" : "base"
      ),
      padding: !1,
      elem_id: (
        /*elem_id*/
        n[1]
      ),
      elem_classes: (
        /*elem_classes*/
        n[2]
      ),
      container: (
        /*container*/
        n[11]
      ),
      scale: (
        /*scale*/
        n[12]
      ),
      min_width: (
        /*min_width*/
        n[13]
      ),
      allow_overflow: !1,
      $$slots: { default: [qu] },
      $$scope: { ctx: n }
    }
  }), {
    c() {
      St(e.$$.fragment);
    },
    m(l, i) {
      zt(e, l, i), t = !0;
    },
    p(l, [i]) {
      const o = {};
      i & /*visible*/
      8 && (o.visible = /*visible*/
      l[3]), i & /*value*/
      1 && (o.variant = /*value*/
      l[0] === null ? "dashed" : "solid"), i & /*dragging*/
      262144 && (o.border_mode = /*dragging*/
      l[18] ? "focus" : "base"), i & /*elem_id*/
      2 && (o.elem_id = /*elem_id*/
      l[1]), i & /*elem_classes*/
      4 && (o.elem_classes = /*elem_classes*/
      l[2]), i & /*container*/
      2048 && (o.container = /*container*/
      l[11]), i & /*scale*/
      4096 && (o.scale = /*scale*/
      l[12]), i & /*min_width*/
      8192 && (o.min_width = /*min_width*/
      l[13]), i & /*$$scope, _selectable, _value, label, show_label, height, gradio, interactive, file_count, file_types, root, value, dragging, loading_status*/
      134727665 && (o.$$scope = { dirty: i, ctx: l }), e.$set(o);
    },
    i(l) {
      t || (nt(e.$$.fragment, l), t = !0);
    },
    o(l) {
      lt(e.$$.fragment, l), t = !1;
    },
    d(l) {
      Ct(e, l);
    }
  };
}
function Cu(n, e, t) {
  let l, { elem_id: i = "" } = e, { elem_classes: o = [] } = e, { visible: s = !0 } = e, { value: f } = e, { interactive: a } = e, { root: r } = e, { label: u } = e, { show_label: c } = e, { height: d = void 0 } = e, { proxy_url: _ } = e, { _selectable: m = !1 } = e, { loading_status: y } = e, { container: q = !0 } = e, { scale: w = null } = e, { min_width: p = void 0 } = e, { gradio: h } = e, { file_count: z } = e, { file_types: F = ["file"] } = e, g = l, D = !1;
  const T = ({ detail: C }) => h.dispatch("select", C), S = ({ detail: C }) => {
    t(0, f = C);
  }, B = ({ detail: C }) => t(18, D = C), I = () => h.dispatch("clear"), W = ({ detail: C }) => h.dispatch("select", C), G = () => h.dispatch("upload");
  return n.$$set = (C) => {
    "elem_id" in C && t(1, i = C.elem_id), "elem_classes" in C && t(2, o = C.elem_classes), "visible" in C && t(3, s = C.visible), "value" in C && t(0, f = C.value), "interactive" in C && t(4, a = C.interactive), "root" in C && t(5, r = C.root), "label" in C && t(6, u = C.label), "show_label" in C && t(7, c = C.show_label), "height" in C && t(8, d = C.height), "proxy_url" in C && t(19, _ = C.proxy_url), "_selectable" in C && t(9, m = C._selectable), "loading_status" in C && t(10, y = C.loading_status), "container" in C && t(11, q = C.container), "scale" in C && t(12, w = C.scale), "min_width" in C && t(13, p = C.min_width), "gradio" in C && t(14, h = C.gradio), "file_count" in C && t(15, z = C.file_count), "file_types" in C && t(16, F = C.file_types);
  }, n.$$.update = () => {
    n.$$.dirty & /*value, root, proxy_url*/
    524321 && t(17, l = Ye(f, r, _)), n.$$.dirty & /*old_value, _value, gradio*/
    1196032 && JSON.stringify(g) !== JSON.stringify(l) && (h.dispatch("change"), t(20, g = l));
  }, [
    f,
    i,
    o,
    s,
    a,
    r,
    u,
    c,
    d,
    m,
    y,
    q,
    w,
    p,
    h,
    z,
    F,
    l,
    D,
    _,
    g,
    T,
    S,
    B,
    I,
    W,
    G
  ];
}
class Lu extends uu {
  constructor(e) {
    super(), pu(this, e, Cu, Su, bu, {
      elem_id: 1,
      elem_classes: 2,
      visible: 3,
      value: 0,
      interactive: 4,
      root: 5,
      label: 6,
      show_label: 7,
      height: 8,
      proxy_url: 19,
      _selectable: 9,
      loading_status: 10,
      container: 11,
      scale: 12,
      min_width: 13,
      gradio: 14,
      file_count: 15,
      file_types: 16
    });
  }
  get elem_id() {
    return this.$$.ctx[1];
  }
  set elem_id(e) {
    this.$$set({ elem_id: e }), $();
  }
  get elem_classes() {
    return this.$$.ctx[2];
  }
  set elem_classes(e) {
    this.$$set({ elem_classes: e }), $();
  }
  get visible() {
    return this.$$.ctx[3];
  }
  set visible(e) {
    this.$$set({ visible: e }), $();
  }
  get value() {
    return this.$$.ctx[0];
  }
  set value(e) {
    this.$$set({ value: e }), $();
  }
  get interactive() {
    return this.$$.ctx[4];
  }
  set interactive(e) {
    this.$$set({ interactive: e }), $();
  }
  get root() {
    return this.$$.ctx[5];
  }
  set root(e) {
    this.$$set({ root: e }), $();
  }
  get label() {
    return this.$$.ctx[6];
  }
  set label(e) {
    this.$$set({ label: e }), $();
  }
  get show_label() {
    return this.$$.ctx[7];
  }
  set show_label(e) {
    this.$$set({ show_label: e }), $();
  }
  get height() {
    return this.$$.ctx[8];
  }
  set height(e) {
    this.$$set({ height: e }), $();
  }
  get proxy_url() {
    return this.$$.ctx[19];
  }
  set proxy_url(e) {
    this.$$set({ proxy_url: e }), $();
  }
  get _selectable() {
    return this.$$.ctx[9];
  }
  set _selectable(e) {
    this.$$set({ _selectable: e }), $();
  }
  get loading_status() {
    return this.$$.ctx[10];
  }
  set loading_status(e) {
    this.$$set({ loading_status: e }), $();
  }
  get container() {
    return this.$$.ctx[11];
  }
  set container(e) {
    this.$$set({ container: e }), $();
  }
  get scale() {
    return this.$$.ctx[12];
  }
  set scale(e) {
    this.$$set({ scale: e }), $();
  }
  get min_width() {
    return this.$$.ctx[13];
  }
  set min_width(e) {
    this.$$set({ min_width: e }), $();
  }
  get gradio() {
    return this.$$.ctx[14];
  }
  set gradio(e) {
    this.$$set({ gradio: e }), $();
  }
  get file_count() {
    return this.$$.ctx[15];
  }
  set file_count(e) {
    this.$$set({ file_count: e }), $();
  }
  get file_types() {
    return this.$$.ctx[16];
  }
  set file_types(e) {
    this.$$set({ file_types: e }), $();
  }
}
export {
  Au as BaseExample,
  Da as BaseFile,
  uf as BaseFileUpload,
  ci as FilePreview,
  Lu as default
};
