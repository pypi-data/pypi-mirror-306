const {
  SvelteComponent: o,
  attr: v,
  detach: y,
  element: g,
  init: m,
  insert: h,
  noop: u,
  safe_not_equal: b,
  toggle_class: i
} = window.__gradio__svelte__internal;
function w(n) {
  let e;
  return {
    c() {
      e = g("div"), e.textContent = `${/*names_string*/
      n[2]}`, v(e, "class", "svelte-1gecy8w"), i(
        e,
        "table",
        /*type*/
        n[0] === "table"
      ), i(
        e,
        "gallery",
        /*type*/
        n[0] === "gallery"
      ), i(
        e,
        "selected",
        /*selected*/
        n[1]
      );
    },
    m(t, l) {
      h(t, e, l);
    },
    p(t, [l]) {
      l & /*type*/
      1 && i(
        e,
        "table",
        /*type*/
        t[0] === "table"
      ), l & /*type*/
      1 && i(
        e,
        "gallery",
        /*type*/
        t[0] === "gallery"
      ), l & /*selected*/
      2 && i(
        e,
        "selected",
        /*selected*/
        t[1]
      );
    },
    i: u,
    o: u,
    d(t) {
      t && y(e);
    }
  };
}
function A(n, e, t) {
  let { value: l } = e, { type: r } = e, { selected: f = !1 } = e, { choices: s } = e, d = (l ? Array.isArray(l) ? l : [l] : []).map((a) => {
    var c;
    return (c = s.find((_) => _[1] === a)) === null || c === void 0 ? void 0 : c[0];
  }).filter((a) => a !== void 0).join(", ");
  return n.$$set = (a) => {
    "value" in a && t(3, l = a.value), "type" in a && t(0, r = a.type), "selected" in a && t(1, f = a.selected), "choices" in a && t(4, s = a.choices);
  }, [r, f, d, l, s];
}
class q extends o {
  constructor(e) {
    super(), m(this, e, A, w, b, {
      value: 3,
      type: 0,
      selected: 1,
      choices: 4
    });
  }
}
export {
  q as default
};
