const {
  SvelteComponent: u,
  append: _,
  attr: d,
  detach: o,
  element: g,
  init: y,
  insert: c,
  noop: f,
  safe_not_equal: v,
  set_data: m,
  text: b,
  toggle_class: r
} = window.__gradio__svelte__internal;
function A(t) {
  let e, n = (Array.isArray(
    /*value*/
    t[0]
  ) ? (
    /*value*/
    t[0].join(", ")
  ) : (
    /*value*/
    t[0]
  )) + "", i;
  return {
    c() {
      e = g("div"), i = b(n), d(e, "class", "svelte-1hgn91n"), r(
        e,
        "table",
        /*type*/
        t[1] === "table"
      ), r(
        e,
        "gallery",
        /*type*/
        t[1] === "gallery"
      ), r(
        e,
        "selected",
        /*selected*/
        t[2]
      );
    },
    m(l, a) {
      c(l, e, a), _(e, i);
    },
    p(l, [a]) {
      a & /*value*/
      1 && n !== (n = (Array.isArray(
        /*value*/
        l[0]
      ) ? (
        /*value*/
        l[0].join(", ")
      ) : (
        /*value*/
        l[0]
      )) + "") && m(i, n), a & /*type*/
      2 && r(
        e,
        "table",
        /*type*/
        l[1] === "table"
      ), a & /*type*/
      2 && r(
        e,
        "gallery",
        /*type*/
        l[1] === "gallery"
      ), a & /*selected*/
      4 && r(
        e,
        "selected",
        /*selected*/
        l[2]
      );
    },
    i: f,
    o: f,
    d(l) {
      l && o(e);
    }
  };
}
function h(t, e, n) {
  let { value: i } = e, { type: l } = e, { selected: a = !1 } = e;
  return t.$$set = (s) => {
    "value" in s && n(0, i = s.value), "type" in s && n(1, l = s.type), "selected" in s && n(2, a = s.selected);
  }, [i, l, a];
}
class j extends u {
  constructor(e) {
    super(), y(this, e, h, A, v, { value: 0, type: 1, selected: 2 });
  }
}
export {
  j as default
};
