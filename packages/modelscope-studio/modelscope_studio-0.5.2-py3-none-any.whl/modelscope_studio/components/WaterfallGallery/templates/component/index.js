var Fi = Object.defineProperty;
var Bi = (n, e, t) => e in n ? Fi(n, e, { enumerable: !0, configurable: !0, writable: !0, value: t }) : n[e] = t;
var yn = (n, e, t) => (Bi(n, typeof e != "symbol" ? e + "" : e, t), t);
const {
  SvelteComponent: Ni,
  assign: Ti,
  create_slot: Vi,
  detach: Pi,
  element: Oi,
  get_all_dirty_from_scope: Wi,
  get_slot_changes: Ui,
  get_spread_update: Zi,
  init: Hi,
  insert: Gi,
  safe_not_equal: Xi,
  set_dynamic_element_data: Cn,
  set_style: x,
  toggle_class: we,
  transition_in: Al,
  transition_out: Rl,
  update_slot_base: Yi
} = window.__gradio__svelte__internal;
function Ki(n) {
  let e, t, l;
  const i = (
    /*#slots*/
    n[18].default
  ), o = Vi(
    i,
    n,
    /*$$scope*/
    n[17],
    null
  );
  let r = [
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
  for (let a = 0; a < r.length; a += 1)
    f = Ti(f, r[a]);
  return {
    c() {
      e = Oi(
        /*tag*/
        n[14]
      ), o && o.c(), Cn(
        /*tag*/
        n[14]
      )(e, f), we(
        e,
        "hidden",
        /*visible*/
        n[10] === !1
      ), we(
        e,
        "padded",
        /*padding*/
        n[6]
      ), we(
        e,
        "border_focus",
        /*border_mode*/
        n[5] === "focus"
      ), we(
        e,
        "border_contrast",
        /*border_mode*/
        n[5] === "contrast"
      ), we(e, "hide-container", !/*explicit_call*/
      n[8] && !/*container*/
      n[9]), x(
        e,
        "height",
        /*get_dimension*/
        n[15](
          /*height*/
          n[0]
        )
      ), x(e, "width", typeof /*width*/
      n[1] == "number" ? `calc(min(${/*width*/
      n[1]}px, 100%))` : (
        /*get_dimension*/
        n[15](
          /*width*/
          n[1]
        )
      )), x(
        e,
        "border-style",
        /*variant*/
        n[4]
      ), x(
        e,
        "overflow",
        /*allow_overflow*/
        n[11] ? "visible" : "hidden"
      ), x(
        e,
        "flex-grow",
        /*scale*/
        n[12]
      ), x(e, "min-width", `calc(min(${/*min_width*/
      n[13]}px, 100%))`), x(e, "border-width", "var(--block-border-width)");
    },
    m(a, s) {
      Gi(a, e, s), o && o.m(e, null), l = !0;
    },
    p(a, s) {
      o && o.p && (!l || s & /*$$scope*/
      131072) && Yi(
        o,
        i,
        a,
        /*$$scope*/
        a[17],
        l ? Ui(
          i,
          /*$$scope*/
          a[17],
          s,
          null
        ) : Wi(
          /*$$scope*/
          a[17]
        ),
        null
      ), Cn(
        /*tag*/
        a[14]
      )(e, f = Zi(r, [
        (!l || s & /*test_id*/
        128) && { "data-testid": (
          /*test_id*/
          a[7]
        ) },
        (!l || s & /*elem_id*/
        4) && { id: (
          /*elem_id*/
          a[2]
        ) },
        (!l || s & /*elem_classes*/
        8 && t !== (t = "block " + /*elem_classes*/
        a[3].join(" ") + " svelte-nl1om8")) && { class: t }
      ])), we(
        e,
        "hidden",
        /*visible*/
        a[10] === !1
      ), we(
        e,
        "padded",
        /*padding*/
        a[6]
      ), we(
        e,
        "border_focus",
        /*border_mode*/
        a[5] === "focus"
      ), we(
        e,
        "border_contrast",
        /*border_mode*/
        a[5] === "contrast"
      ), we(e, "hide-container", !/*explicit_call*/
      a[8] && !/*container*/
      a[9]), s & /*height*/
      1 && x(
        e,
        "height",
        /*get_dimension*/
        a[15](
          /*height*/
          a[0]
        )
      ), s & /*width*/
      2 && x(e, "width", typeof /*width*/
      a[1] == "number" ? `calc(min(${/*width*/
      a[1]}px, 100%))` : (
        /*get_dimension*/
        a[15](
          /*width*/
          a[1]
        )
      )), s & /*variant*/
      16 && x(
        e,
        "border-style",
        /*variant*/
        a[4]
      ), s & /*allow_overflow*/
      2048 && x(
        e,
        "overflow",
        /*allow_overflow*/
        a[11] ? "visible" : "hidden"
      ), s & /*scale*/
      4096 && x(
        e,
        "flex-grow",
        /*scale*/
        a[12]
      ), s & /*min_width*/
      8192 && x(e, "min-width", `calc(min(${/*min_width*/
      a[13]}px, 100%))`);
    },
    i(a) {
      l || (Al(o, a), l = !0);
    },
    o(a) {
      Rl(o, a), l = !1;
    },
    d(a) {
      a && Pi(e), o && o.d(a);
    }
  };
}
function Ji(n) {
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
      e || (Al(t, l), e = !0);
    },
    o(l) {
      Rl(t, l), e = !1;
    },
    d(l) {
      t && t.d(l);
    }
  };
}
function Qi(n, e, t) {
  let { $$slots: l = {}, $$scope: i } = e, { height: o = void 0 } = e, { width: r = void 0 } = e, { elem_id: f = "" } = e, { elem_classes: a = [] } = e, { variant: s = "solid" } = e, { border_mode: u = "base" } = e, { padding: _ = !0 } = e, { type: c = "normal" } = e, { test_id: d = void 0 } = e, { explicit_call: h = !1 } = e, { container: y = !0 } = e, { visible: S = !0 } = e, { allow_overflow: v = !0 } = e, { scale: k = null } = e, { min_width: p = 0 } = e, b = c === "fieldset" ? "fieldset" : "div";
  const q = (g) => {
    if (g !== void 0) {
      if (typeof g == "number")
        return g + "px";
      if (typeof g == "string")
        return g;
    }
  };
  return n.$$set = (g) => {
    "height" in g && t(0, o = g.height), "width" in g && t(1, r = g.width), "elem_id" in g && t(2, f = g.elem_id), "elem_classes" in g && t(3, a = g.elem_classes), "variant" in g && t(4, s = g.variant), "border_mode" in g && t(5, u = g.border_mode), "padding" in g && t(6, _ = g.padding), "type" in g && t(16, c = g.type), "test_id" in g && t(7, d = g.test_id), "explicit_call" in g && t(8, h = g.explicit_call), "container" in g && t(9, y = g.container), "visible" in g && t(10, S = g.visible), "allow_overflow" in g && t(11, v = g.allow_overflow), "scale" in g && t(12, k = g.scale), "min_width" in g && t(13, p = g.min_width), "$$scope" in g && t(17, i = g.$$scope);
  }, [
    o,
    r,
    f,
    a,
    s,
    u,
    _,
    d,
    h,
    y,
    S,
    v,
    k,
    p,
    b,
    q,
    c,
    i,
    l
  ];
}
class xi extends Ni {
  constructor(e) {
    super(), Hi(this, e, Qi, Ji, Xi, {
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
  SvelteComponent: $i,
  append: Ft,
  attr: _t,
  create_component: eo,
  destroy_component: to,
  detach: no,
  element: qn,
  init: lo,
  insert: io,
  mount_component: oo,
  safe_not_equal: so,
  set_data: ao,
  space: ro,
  text: fo,
  toggle_class: Re,
  transition_in: uo,
  transition_out: _o
} = window.__gradio__svelte__internal;
function co(n) {
  let e, t, l, i, o, r;
  return l = new /*Icon*/
  n[1]({}), {
    c() {
      e = qn("label"), t = qn("span"), eo(l.$$.fragment), i = ro(), o = fo(
        /*label*/
        n[0]
      ), _t(t, "class", "svelte-9gxdi0"), _t(e, "for", ""), _t(e, "data-testid", "block-label"), _t(e, "class", "svelte-9gxdi0"), Re(e, "hide", !/*show_label*/
      n[2]), Re(e, "sr-only", !/*show_label*/
      n[2]), Re(
        e,
        "float",
        /*float*/
        n[4]
      ), Re(
        e,
        "hide-label",
        /*disable*/
        n[3]
      );
    },
    m(f, a) {
      io(f, e, a), Ft(e, t), oo(l, t, null), Ft(e, i), Ft(e, o), r = !0;
    },
    p(f, [a]) {
      (!r || a & /*label*/
      1) && ao(
        o,
        /*label*/
        f[0]
      ), (!r || a & /*show_label*/
      4) && Re(e, "hide", !/*show_label*/
      f[2]), (!r || a & /*show_label*/
      4) && Re(e, "sr-only", !/*show_label*/
      f[2]), (!r || a & /*float*/
      16) && Re(
        e,
        "float",
        /*float*/
        f[4]
      ), (!r || a & /*disable*/
      8) && Re(
        e,
        "hide-label",
        /*disable*/
        f[3]
      );
    },
    i(f) {
      r || (uo(l.$$.fragment, f), r = !0);
    },
    o(f) {
      _o(l.$$.fragment, f), r = !1;
    },
    d(f) {
      f && no(e), to(l);
    }
  };
}
function mo(n, e, t) {
  let { label: l = null } = e, { Icon: i } = e, { show_label: o = !0 } = e, { disable: r = !1 } = e, { float: f = !0 } = e;
  return n.$$set = (a) => {
    "label" in a && t(0, l = a.label), "Icon" in a && t(1, i = a.Icon), "show_label" in a && t(2, o = a.show_label), "disable" in a && t(3, r = a.disable), "float" in a && t(4, f = a.float);
  }, [l, i, o, r, f];
}
class ho extends $i {
  constructor(e) {
    super(), lo(this, e, mo, co, so, {
      label: 0,
      Icon: 1,
      show_label: 2,
      disable: 3,
      float: 4
    });
  }
}
const {
  SvelteComponent: bo,
  append: nn,
  attr: Le,
  bubble: go,
  create_component: wo,
  destroy_component: ko,
  detach: Dl,
  element: ln,
  init: po,
  insert: Fl,
  listen: vo,
  mount_component: yo,
  safe_not_equal: Co,
  set_data: qo,
  set_style: Ge,
  space: So,
  text: Lo,
  toggle_class: Y,
  transition_in: Eo,
  transition_out: zo
} = window.__gradio__svelte__internal;
function Sn(n) {
  let e, t;
  return {
    c() {
      e = ln("span"), t = Lo(
        /*label*/
        n[1]
      ), Le(e, "class", "svelte-1lrphxw");
    },
    m(l, i) {
      Fl(l, e, i), nn(e, t);
    },
    p(l, i) {
      i & /*label*/
      2 && qo(
        t,
        /*label*/
        l[1]
      );
    },
    d(l) {
      l && Dl(e);
    }
  };
}
function jo(n) {
  let e, t, l, i, o, r, f, a = (
    /*show_label*/
    n[2] && Sn(n)
  );
  return i = new /*Icon*/
  n[0]({}), {
    c() {
      e = ln("button"), a && a.c(), t = So(), l = ln("div"), wo(i.$$.fragment), Le(l, "class", "svelte-1lrphxw"), Y(
        l,
        "small",
        /*size*/
        n[4] === "small"
      ), Y(
        l,
        "large",
        /*size*/
        n[4] === "large"
      ), Y(
        l,
        "medium",
        /*size*/
        n[4] === "medium"
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
      ), Le(e, "class", "svelte-1lrphxw"), Y(
        e,
        "pending",
        /*pending*/
        n[3]
      ), Y(
        e,
        "padded",
        /*padded*/
        n[5]
      ), Y(
        e,
        "highlight",
        /*highlight*/
        n[6]
      ), Y(
        e,
        "transparent",
        /*transparent*/
        n[9]
      ), Ge(e, "color", !/*disabled*/
      n[7] && /*_color*/
      n[12] ? (
        /*_color*/
        n[12]
      ) : "var(--block-label-text-color)"), Ge(e, "--bg-color", /*disabled*/
      n[7] ? "auto" : (
        /*background*/
        n[10]
      )), Ge(
        e,
        "margin-left",
        /*offset*/
        n[11] + "px"
      );
    },
    m(s, u) {
      Fl(s, e, u), a && a.m(e, null), nn(e, t), nn(e, l), yo(i, l, null), o = !0, r || (f = vo(
        e,
        "click",
        /*click_handler*/
        n[14]
      ), r = !0);
    },
    p(s, [u]) {
      /*show_label*/
      s[2] ? a ? a.p(s, u) : (a = Sn(s), a.c(), a.m(e, t)) : a && (a.d(1), a = null), (!o || u & /*size*/
      16) && Y(
        l,
        "small",
        /*size*/
        s[4] === "small"
      ), (!o || u & /*size*/
      16) && Y(
        l,
        "large",
        /*size*/
        s[4] === "large"
      ), (!o || u & /*size*/
      16) && Y(
        l,
        "medium",
        /*size*/
        s[4] === "medium"
      ), (!o || u & /*disabled*/
      128) && (e.disabled = /*disabled*/
      s[7]), (!o || u & /*label*/
      2) && Le(
        e,
        "aria-label",
        /*label*/
        s[1]
      ), (!o || u & /*hasPopup*/
      256) && Le(
        e,
        "aria-haspopup",
        /*hasPopup*/
        s[8]
      ), (!o || u & /*label*/
      2) && Le(
        e,
        "title",
        /*label*/
        s[1]
      ), (!o || u & /*pending*/
      8) && Y(
        e,
        "pending",
        /*pending*/
        s[3]
      ), (!o || u & /*padded*/
      32) && Y(
        e,
        "padded",
        /*padded*/
        s[5]
      ), (!o || u & /*highlight*/
      64) && Y(
        e,
        "highlight",
        /*highlight*/
        s[6]
      ), (!o || u & /*transparent*/
      512) && Y(
        e,
        "transparent",
        /*transparent*/
        s[9]
      ), u & /*disabled, _color*/
      4224 && Ge(e, "color", !/*disabled*/
      s[7] && /*_color*/
      s[12] ? (
        /*_color*/
        s[12]
      ) : "var(--block-label-text-color)"), u & /*disabled, background*/
      1152 && Ge(e, "--bg-color", /*disabled*/
      s[7] ? "auto" : (
        /*background*/
        s[10]
      )), u & /*offset*/
      2048 && Ge(
        e,
        "margin-left",
        /*offset*/
        s[11] + "px"
      );
    },
    i(s) {
      o || (Eo(i.$$.fragment, s), o = !0);
    },
    o(s) {
      zo(i.$$.fragment, s), o = !1;
    },
    d(s) {
      s && Dl(e), a && a.d(), ko(i), r = !1, f();
    }
  };
}
function Io(n, e, t) {
  let l, { Icon: i } = e, { label: o = "" } = e, { show_label: r = !1 } = e, { pending: f = !1 } = e, { size: a = "small" } = e, { padded: s = !0 } = e, { highlight: u = !1 } = e, { disabled: _ = !1 } = e, { hasPopup: c = !1 } = e, { color: d = "var(--block-label-text-color)" } = e, { transparent: h = !1 } = e, { background: y = "var(--background-fill-primary)" } = e, { offset: S = 0 } = e;
  function v(k) {
    go.call(this, n, k);
  }
  return n.$$set = (k) => {
    "Icon" in k && t(0, i = k.Icon), "label" in k && t(1, o = k.label), "show_label" in k && t(2, r = k.show_label), "pending" in k && t(3, f = k.pending), "size" in k && t(4, a = k.size), "padded" in k && t(5, s = k.padded), "highlight" in k && t(6, u = k.highlight), "disabled" in k && t(7, _ = k.disabled), "hasPopup" in k && t(8, c = k.hasPopup), "color" in k && t(13, d = k.color), "transparent" in k && t(9, h = k.transparent), "background" in k && t(10, y = k.background), "offset" in k && t(11, S = k.offset);
  }, n.$$.update = () => {
    n.$$.dirty & /*highlight, color*/
    8256 && t(12, l = u ? "var(--color-accent)" : d);
  }, [
    i,
    o,
    r,
    f,
    a,
    s,
    u,
    _,
    c,
    h,
    y,
    S,
    l,
    d,
    v
  ];
}
class ze extends bo {
  constructor(e) {
    super(), po(this, e, Io, jo, Co, {
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
}
const {
  SvelteComponent: Mo,
  append: Ao,
  attr: Bt,
  binding_callbacks: Ro,
  create_slot: Do,
  detach: Fo,
  element: Ln,
  get_all_dirty_from_scope: Bo,
  get_slot_changes: No,
  init: To,
  insert: Vo,
  safe_not_equal: Po,
  toggle_class: De,
  transition_in: Oo,
  transition_out: Wo,
  update_slot_base: Uo
} = window.__gradio__svelte__internal;
function Zo(n) {
  let e, t, l;
  const i = (
    /*#slots*/
    n[5].default
  ), o = Do(
    i,
    n,
    /*$$scope*/
    n[4],
    null
  );
  return {
    c() {
      e = Ln("div"), t = Ln("div"), o && o.c(), Bt(t, "class", "icon svelte-3w3rth"), Bt(e, "class", "empty svelte-3w3rth"), Bt(e, "aria-label", "Empty value"), De(
        e,
        "small",
        /*size*/
        n[0] === "small"
      ), De(
        e,
        "large",
        /*size*/
        n[0] === "large"
      ), De(
        e,
        "unpadded_box",
        /*unpadded_box*/
        n[1]
      ), De(
        e,
        "small_parent",
        /*parent_height*/
        n[3]
      );
    },
    m(r, f) {
      Vo(r, e, f), Ao(e, t), o && o.m(t, null), n[6](e), l = !0;
    },
    p(r, [f]) {
      o && o.p && (!l || f & /*$$scope*/
      16) && Uo(
        o,
        i,
        r,
        /*$$scope*/
        r[4],
        l ? No(
          i,
          /*$$scope*/
          r[4],
          f,
          null
        ) : Bo(
          /*$$scope*/
          r[4]
        ),
        null
      ), (!l || f & /*size*/
      1) && De(
        e,
        "small",
        /*size*/
        r[0] === "small"
      ), (!l || f & /*size*/
      1) && De(
        e,
        "large",
        /*size*/
        r[0] === "large"
      ), (!l || f & /*unpadded_box*/
      2) && De(
        e,
        "unpadded_box",
        /*unpadded_box*/
        r[1]
      ), (!l || f & /*parent_height*/
      8) && De(
        e,
        "small_parent",
        /*parent_height*/
        r[3]
      );
    },
    i(r) {
      l || (Oo(o, r), l = !0);
    },
    o(r) {
      Wo(o, r), l = !1;
    },
    d(r) {
      r && Fo(e), o && o.d(r), n[6](null);
    }
  };
}
function Ho(n, e, t) {
  let l, { $$slots: i = {}, $$scope: o } = e, { size: r = "small" } = e, { unpadded_box: f = !1 } = e, a;
  function s(_) {
    var h;
    if (!_)
      return !1;
    const { height: c } = _.getBoundingClientRect(), { height: d } = ((h = _.parentElement) == null ? void 0 : h.getBoundingClientRect()) || { height: c };
    return c > d + 2;
  }
  function u(_) {
    Ro[_ ? "unshift" : "push"](() => {
      a = _, t(2, a);
    });
  }
  return n.$$set = (_) => {
    "size" in _ && t(0, r = _.size), "unpadded_box" in _ && t(1, f = _.unpadded_box), "$$scope" in _ && t(4, o = _.$$scope);
  }, n.$$.update = () => {
    n.$$.dirty & /*el*/
    4 && t(3, l = s(a));
  }, [r, f, a, l, o, i, u];
}
class Go extends Mo {
  constructor(e) {
    super(), To(this, e, Ho, Zo, Po, { size: 0, unpadded_box: 1 });
  }
}
const {
  SvelteComponent: Xo,
  append: Nt,
  attr: oe,
  detach: Yo,
  init: Ko,
  insert: Jo,
  noop: Tt,
  safe_not_equal: Qo,
  set_style: ke,
  svg_element: ct
} = window.__gradio__svelte__internal;
function xo(n) {
  let e, t, l, i;
  return {
    c() {
      e = ct("svg"), t = ct("g"), l = ct("path"), i = ct("path"), oe(l, "d", "M18,6L6.087,17.913"), ke(l, "fill", "none"), ke(l, "fill-rule", "nonzero"), ke(l, "stroke-width", "2px"), oe(t, "transform", "matrix(1.14096,-0.140958,-0.140958,1.14096,-0.0559523,0.0559523)"), oe(i, "d", "M4.364,4.364L19.636,19.636"), ke(i, "fill", "none"), ke(i, "fill-rule", "nonzero"), ke(i, "stroke-width", "2px"), oe(e, "width", "100%"), oe(e, "height", "100%"), oe(e, "viewBox", "0 0 24 24"), oe(e, "version", "1.1"), oe(e, "xmlns", "http://www.w3.org/2000/svg"), oe(e, "xmlns:xlink", "http://www.w3.org/1999/xlink"), oe(e, "xml:space", "preserve"), oe(e, "stroke", "currentColor"), ke(e, "fill-rule", "evenodd"), ke(e, "clip-rule", "evenodd"), ke(e, "stroke-linecap", "round"), ke(e, "stroke-linejoin", "round");
    },
    m(o, r) {
      Jo(o, e, r), Nt(e, t), Nt(t, l), Nt(e, i);
    },
    p: Tt,
    i: Tt,
    o: Tt,
    d(o) {
      o && Yo(e);
    }
  };
}
class Bl extends Xo {
  constructor(e) {
    super(), Ko(this, e, null, xo, Qo, {});
  }
}
const {
  SvelteComponent: $o,
  append: es,
  attr: tt,
  detach: ts,
  init: ns,
  insert: ls,
  noop: Vt,
  safe_not_equal: is,
  svg_element: En
} = window.__gradio__svelte__internal;
function os(n) {
  let e, t;
  return {
    c() {
      e = En("svg"), t = En("path"), tt(t, "d", "M23,20a5,5,0,0,0-3.89,1.89L11.8,17.32a4.46,4.46,0,0,0,0-2.64l7.31-4.57A5,5,0,1,0,18,7a4.79,4.79,0,0,0,.2,1.32l-7.31,4.57a5,5,0,1,0,0,6.22l7.31,4.57A4.79,4.79,0,0,0,18,25a5,5,0,1,0,5-5ZM23,4a3,3,0,1,1-3,3A3,3,0,0,1,23,4ZM7,19a3,3,0,1,1,3-3A3,3,0,0,1,7,19Zm16,9a3,3,0,1,1,3-3A3,3,0,0,1,23,28Z"), tt(t, "fill", "currentColor"), tt(e, "id", "icon"), tt(e, "xmlns", "http://www.w3.org/2000/svg"), tt(e, "viewBox", "0 0 32 32");
    },
    m(l, i) {
      ls(l, e, i), es(e, t);
    },
    p: Vt,
    i: Vt,
    o: Vt,
    d(l) {
      l && ts(e);
    }
  };
}
class ss extends $o {
  constructor(e) {
    super(), ns(this, e, null, os, is, {});
  }
}
const {
  SvelteComponent: as,
  append: rs,
  attr: Xe,
  detach: fs,
  init: us,
  insert: _s,
  noop: Pt,
  safe_not_equal: cs,
  svg_element: zn
} = window.__gradio__svelte__internal;
function ds(n) {
  let e, t;
  return {
    c() {
      e = zn("svg"), t = zn("path"), Xe(t, "fill", "currentColor"), Xe(t, "d", "M26 24v4H6v-4H4v4a2 2 0 0 0 2 2h20a2 2 0 0 0 2-2v-4zm0-10l-1.41-1.41L17 20.17V2h-2v18.17l-7.59-7.58L6 14l10 10l10-10z"), Xe(e, "xmlns", "http://www.w3.org/2000/svg"), Xe(e, "width", "100%"), Xe(e, "height", "100%"), Xe(e, "viewBox", "0 0 32 32");
    },
    m(l, i) {
      _s(l, e, i), rs(e, t);
    },
    p: Pt,
    i: Pt,
    o: Pt,
    d(l) {
      l && fs(e);
    }
  };
}
class Nl extends as {
  constructor(e) {
    super(), us(this, e, null, ds, cs, {});
  }
}
const {
  SvelteComponent: ms,
  append: hs,
  attr: se,
  detach: bs,
  init: gs,
  insert: ws,
  noop: Ot,
  safe_not_equal: ks,
  svg_element: jn
} = window.__gradio__svelte__internal;
function ps(n) {
  let e, t;
  return {
    c() {
      e = jn("svg"), t = jn("path"), se(t, "d", "M17 3a2.828 2.828 0 1 1 4 4L7.5 20.5 2 22l1.5-5.5L17 3z"), se(e, "xmlns", "http://www.w3.org/2000/svg"), se(e, "width", "100%"), se(e, "height", "100%"), se(e, "viewBox", "0 0 24 24"), se(e, "fill", "none"), se(e, "stroke", "currentColor"), se(e, "stroke-width", "1.5"), se(e, "stroke-linecap", "round"), se(e, "stroke-linejoin", "round"), se(e, "class", "feather feather-edit-2");
    },
    m(l, i) {
      ws(l, e, i), hs(e, t);
    },
    p: Ot,
    i: Ot,
    o: Ot,
    d(l) {
      l && bs(e);
    }
  };
}
class vs extends ms {
  constructor(e) {
    super(), gs(this, e, null, ps, ks, {});
  }
}
const {
  SvelteComponent: ys,
  append: Wt,
  attr: T,
  detach: Cs,
  init: qs,
  insert: Ss,
  noop: Ut,
  safe_not_equal: Ls,
  svg_element: dt
} = window.__gradio__svelte__internal;
function Es(n) {
  let e, t, l, i;
  return {
    c() {
      e = dt("svg"), t = dt("rect"), l = dt("circle"), i = dt("polyline"), T(t, "x", "3"), T(t, "y", "3"), T(t, "width", "18"), T(t, "height", "18"), T(t, "rx", "2"), T(t, "ry", "2"), T(l, "cx", "8.5"), T(l, "cy", "8.5"), T(l, "r", "1.5"), T(i, "points", "21 15 16 10 5 21"), T(e, "xmlns", "http://www.w3.org/2000/svg"), T(e, "width", "100%"), T(e, "height", "100%"), T(e, "viewBox", "0 0 24 24"), T(e, "fill", "none"), T(e, "stroke", "currentColor"), T(e, "stroke-width", "1.5"), T(e, "stroke-linecap", "round"), T(e, "stroke-linejoin", "round"), T(e, "class", "feather feather-image");
    },
    m(o, r) {
      Ss(o, e, r), Wt(e, t), Wt(e, l), Wt(e, i);
    },
    p: Ut,
    i: Ut,
    o: Ut,
    d(o) {
      o && Cs(e);
    }
  };
}
let Tl = class extends ys {
  constructor(e) {
    super(), qs(this, e, null, Es, Ls, {});
  }
};
const {
  SvelteComponent: zs,
  append: In,
  attr: G,
  detach: js,
  init: Is,
  insert: Ms,
  noop: Mn,
  safe_not_equal: As,
  svg_element: Zt
} = window.__gradio__svelte__internal;
function Rs(n) {
  let e, t, l, i;
  return {
    c() {
      e = Zt("svg"), t = Zt("path"), l = Zt("path"), G(t, "stroke", "currentColor"), G(t, "stroke-width", "1.5"), G(t, "stroke-linecap", "round"), G(t, "d", "M16.472 20H4.1a.6.6 0 0 1-.6-.6V9.6a.6.6 0 0 1 .6-.6h2.768a2 2 0 0 0 1.715-.971l2.71-4.517a1.631 1.631 0 0 1 2.961 1.308l-1.022 3.408a.6.6 0 0 0 .574.772h4.575a2 2 0 0 1 1.93 2.526l-1.91 7A2 2 0 0 1 16.473 20Z"), G(l, "stroke", "currentColor"), G(l, "stroke-width", "1.5"), G(l, "stroke-linecap", "round"), G(l, "stroke-linejoin", "round"), G(l, "d", "M7 20V9"), G(e, "xmlns", "http://www.w3.org/2000/svg"), G(e, "viewBox", "0 0 24 24"), G(e, "fill", i = /*selected*/
      n[0] ? "currentColor" : "none"), G(e, "stroke-width", "1.5"), G(e, "color", "currentColor");
    },
    m(o, r) {
      Ms(o, e, r), In(e, t), In(e, l);
    },
    p(o, [r]) {
      r & /*selected*/
      1 && i !== (i = /*selected*/
      o[0] ? "currentColor" : "none") && G(e, "fill", i);
    },
    i: Mn,
    o: Mn,
    d(o) {
      o && js(e);
    }
  };
}
function Ds(n, e, t) {
  let { selected: l } = e;
  return n.$$set = (i) => {
    "selected" in i && t(0, l = i.selected);
  }, [l];
}
class Fs extends zs {
  constructor(e) {
    super(), Is(this, e, Ds, Rs, As, { selected: 0 });
  }
}
const {
  SvelteComponent: Bs,
  append: An,
  attr: $,
  detach: Ns,
  init: Ts,
  insert: Vs,
  noop: Ht,
  safe_not_equal: Ps,
  svg_element: Gt
} = window.__gradio__svelte__internal;
function Os(n) {
  let e, t, l;
  return {
    c() {
      e = Gt("svg"), t = Gt("polyline"), l = Gt("path"), $(t, "points", "1 4 1 10 7 10"), $(l, "d", "M3.51 15a9 9 0 1 0 2.13-9.36L1 10"), $(e, "xmlns", "http://www.w3.org/2000/svg"), $(e, "width", "100%"), $(e, "height", "100%"), $(e, "viewBox", "0 0 24 24"), $(e, "fill", "none"), $(e, "stroke", "currentColor"), $(e, "stroke-width", "2"), $(e, "stroke-linecap", "round"), $(e, "stroke-linejoin", "round"), $(e, "class", "feather feather-rotate-ccw");
    },
    m(i, o) {
      Vs(i, e, o), An(e, t), An(e, l);
    },
    p: Ht,
    i: Ht,
    o: Ht,
    d(i) {
      i && Ns(e);
    }
  };
}
class Ws extends Bs {
  constructor(e) {
    super(), Ts(this, e, null, Os, Ps, {});
  }
}
const Us = [
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
], Rn = {
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
Us.reduce(
  (n, { color: e, primary: t, secondary: l }) => ({
    ...n,
    [e]: {
      primary: Rn[e][t],
      secondary: Rn[e][l]
    }
  }),
  {}
);
class Zs extends Error {
  constructor(e) {
    super(e), this.name = "ShareError";
  }
}
const {
  SvelteComponent: Hs,
  create_component: Gs,
  destroy_component: Xs,
  init: Ys,
  mount_component: Ks,
  safe_not_equal: Js,
  transition_in: Qs,
  transition_out: xs
} = window.__gradio__svelte__internal, { createEventDispatcher: $s } = window.__gradio__svelte__internal;
function ea(n) {
  let e, t;
  return e = new ze({
    props: {
      Icon: ss,
      label: (
        /*i18n*/
        n[2]("common.share")
      ),
      pending: (
        /*pending*/
        n[3]
      )
    }
  }), e.$on(
    "click",
    /*click_handler*/
    n[5]
  ), {
    c() {
      Gs(e.$$.fragment);
    },
    m(l, i) {
      Ks(e, l, i), t = !0;
    },
    p(l, [i]) {
      const o = {};
      i & /*i18n*/
      4 && (o.label = /*i18n*/
      l[2]("common.share")), i & /*pending*/
      8 && (o.pending = /*pending*/
      l[3]), e.$set(o);
    },
    i(l) {
      t || (Qs(e.$$.fragment, l), t = !0);
    },
    o(l) {
      xs(e.$$.fragment, l), t = !1;
    },
    d(l) {
      Xs(e, l);
    }
  };
}
function ta(n, e, t) {
  const l = $s();
  let { formatter: i } = e, { value: o } = e, { i18n: r } = e, f = !1;
  const a = async () => {
    try {
      t(3, f = !0);
      const s = await i(o);
      l("share", { description: s });
    } catch (s) {
      console.error(s);
      let u = s instanceof Zs ? s.message : "Share failed.";
      l("error", u);
    } finally {
      t(3, f = !1);
    }
  };
  return n.$$set = (s) => {
    "formatter" in s && t(0, i = s.formatter), "value" in s && t(1, o = s.value), "i18n" in s && t(2, r = s.i18n);
  }, [i, o, r, f, l, a];
}
class na extends Hs {
  constructor(e) {
    super(), Ys(this, e, ta, ea, Js, { formatter: 0, value: 1, i18n: 2 });
  }
}
function Ke(n) {
  let e = ["", "k", "M", "G", "T", "P", "E", "Z"], t = 0;
  for (; n > 1e3 && t < e.length - 1; )
    n /= 1e3, t++;
  let l = e[t];
  return (Number.isInteger(n) ? n : n.toFixed(1)) + l;
}
function gt() {
}
function la(n, e) {
  return n != n ? e == e : n !== e || n && typeof n == "object" || typeof n == "function";
}
const Vl = typeof window < "u";
let Dn = Vl ? () => window.performance.now() : () => Date.now(), Pl = Vl ? (n) => requestAnimationFrame(n) : gt;
const xe = /* @__PURE__ */ new Set();
function Ol(n) {
  xe.forEach((e) => {
    e.c(n) || (xe.delete(e), e.f());
  }), xe.size !== 0 && Pl(Ol);
}
function ia(n) {
  let e;
  return xe.size === 0 && Pl(Ol), {
    promise: new Promise((t) => {
      xe.add(e = { c: n, f: t });
    }),
    abort() {
      xe.delete(e);
    }
  };
}
const Ye = [];
function oa(n, e = gt) {
  let t;
  const l = /* @__PURE__ */ new Set();
  function i(f) {
    if (la(n, f) && (n = f, t)) {
      const a = !Ye.length;
      for (const s of l)
        s[1](), Ye.push(s, n);
      if (a) {
        for (let s = 0; s < Ye.length; s += 2)
          Ye[s][0](Ye[s + 1]);
        Ye.length = 0;
      }
    }
  }
  function o(f) {
    i(f(n));
  }
  function r(f, a = gt) {
    const s = [f, a];
    return l.add(s), l.size === 1 && (t = e(i, o) || gt), f(n), () => {
      l.delete(s), l.size === 0 && t && (t(), t = null);
    };
  }
  return { set: i, update: o, subscribe: r };
}
function Fn(n) {
  return Object.prototype.toString.call(n) === "[object Date]";
}
function on(n, e, t, l) {
  if (typeof t == "number" || Fn(t)) {
    const i = l - t, o = (t - e) / (n.dt || 1 / 60), r = n.opts.stiffness * i, f = n.opts.damping * o, a = (r - f) * n.inv_mass, s = (o + a) * n.dt;
    return Math.abs(s) < n.opts.precision && Math.abs(i) < n.opts.precision ? l : (n.settled = !1, Fn(t) ? new Date(t.getTime() + s) : t + s);
  } else {
    if (Array.isArray(t))
      return t.map(
        (i, o) => on(n, e[o], t[o], l[o])
      );
    if (typeof t == "object") {
      const i = {};
      for (const o in t)
        i[o] = on(n, e[o], t[o], l[o]);
      return i;
    } else
      throw new Error(`Cannot spring ${typeof t} values`);
  }
}
function Bn(n, e = {}) {
  const t = oa(n), { stiffness: l = 0.15, damping: i = 0.8, precision: o = 0.01 } = e;
  let r, f, a, s = n, u = n, _ = 1, c = 0, d = !1;
  function h(S, v = {}) {
    u = S;
    const k = a = {};
    return n == null || v.hard || y.stiffness >= 1 && y.damping >= 1 ? (d = !0, r = Dn(), s = S, t.set(n = u), Promise.resolve()) : (v.soft && (c = 1 / ((v.soft === !0 ? 0.5 : +v.soft) * 60), _ = 0), f || (r = Dn(), d = !1, f = ia((p) => {
      if (d)
        return d = !1, f = null, !1;
      _ = Math.min(_ + c, 1);
      const b = {
        inv_mass: _,
        opts: y,
        settled: !0,
        dt: (p - r) * 60 / 1e3
      }, q = on(b, s, n, u);
      return r = p, s = n, t.set(n = q), b.settled && (f = null), !b.settled;
    })), new Promise((p) => {
      f.promise.then(() => {
        k === a && p();
      });
    }));
  }
  const y = {
    set: h,
    update: (S, v) => h(S(u, n), v),
    subscribe: t.subscribe,
    stiffness: l,
    damping: i,
    precision: o
  };
  return y;
}
const {
  SvelteComponent: sa,
  append: ae,
  attr: I,
  component_subscribe: Nn,
  detach: aa,
  element: ra,
  init: fa,
  insert: ua,
  noop: Tn,
  safe_not_equal: _a,
  set_style: mt,
  svg_element: re,
  toggle_class: Vn
} = window.__gradio__svelte__internal, { onMount: ca } = window.__gradio__svelte__internal;
function da(n) {
  let e, t, l, i, o, r, f, a, s, u, _, c;
  return {
    c() {
      e = ra("div"), t = re("svg"), l = re("g"), i = re("path"), o = re("path"), r = re("path"), f = re("path"), a = re("g"), s = re("path"), u = re("path"), _ = re("path"), c = re("path"), I(i, "d", "M255.926 0.754768L509.702 139.936V221.027L255.926 81.8465V0.754768Z"), I(i, "fill", "#FF7C00"), I(i, "fill-opacity", "0.4"), I(i, "class", "svelte-43sxxs"), I(o, "d", "M509.69 139.936L254.981 279.641V361.255L509.69 221.55V139.936Z"), I(o, "fill", "#FF7C00"), I(o, "class", "svelte-43sxxs"), I(r, "d", "M0.250138 139.937L254.981 279.641V361.255L0.250138 221.55V139.937Z"), I(r, "fill", "#FF7C00"), I(r, "fill-opacity", "0.4"), I(r, "class", "svelte-43sxxs"), I(f, "d", "M255.923 0.232622L0.236328 139.936V221.55L255.923 81.8469V0.232622Z"), I(f, "fill", "#FF7C00"), I(f, "class", "svelte-43sxxs"), mt(l, "transform", "translate(" + /*$top*/
      n[1][0] + "px, " + /*$top*/
      n[1][1] + "px)"), I(s, "d", "M255.926 141.5L509.702 280.681V361.773L255.926 222.592V141.5Z"), I(s, "fill", "#FF7C00"), I(s, "fill-opacity", "0.4"), I(s, "class", "svelte-43sxxs"), I(u, "d", "M509.69 280.679L254.981 420.384V501.998L509.69 362.293V280.679Z"), I(u, "fill", "#FF7C00"), I(u, "class", "svelte-43sxxs"), I(_, "d", "M0.250138 280.681L254.981 420.386V502L0.250138 362.295V280.681Z"), I(_, "fill", "#FF7C00"), I(_, "fill-opacity", "0.4"), I(_, "class", "svelte-43sxxs"), I(c, "d", "M255.923 140.977L0.236328 280.68V362.294L255.923 222.591V140.977Z"), I(c, "fill", "#FF7C00"), I(c, "class", "svelte-43sxxs"), mt(a, "transform", "translate(" + /*$bottom*/
      n[2][0] + "px, " + /*$bottom*/
      n[2][1] + "px)"), I(t, "viewBox", "-1200 -1200 3000 3000"), I(t, "fill", "none"), I(t, "xmlns", "http://www.w3.org/2000/svg"), I(t, "class", "svelte-43sxxs"), I(e, "class", "svelte-43sxxs"), Vn(
        e,
        "margin",
        /*margin*/
        n[0]
      );
    },
    m(d, h) {
      ua(d, e, h), ae(e, t), ae(t, l), ae(l, i), ae(l, o), ae(l, r), ae(l, f), ae(t, a), ae(a, s), ae(a, u), ae(a, _), ae(a, c);
    },
    p(d, [h]) {
      h & /*$top*/
      2 && mt(l, "transform", "translate(" + /*$top*/
      d[1][0] + "px, " + /*$top*/
      d[1][1] + "px)"), h & /*$bottom*/
      4 && mt(a, "transform", "translate(" + /*$bottom*/
      d[2][0] + "px, " + /*$bottom*/
      d[2][1] + "px)"), h & /*margin*/
      1 && Vn(
        e,
        "margin",
        /*margin*/
        d[0]
      );
    },
    i: Tn,
    o: Tn,
    d(d) {
      d && aa(e);
    }
  };
}
function ma(n, e, t) {
  let l, i, { margin: o = !0 } = e;
  const r = Bn([0, 0]);
  Nn(n, r, (c) => t(1, l = c));
  const f = Bn([0, 0]);
  Nn(n, f, (c) => t(2, i = c));
  let a;
  async function s() {
    await Promise.all([r.set([125, 140]), f.set([-125, -140])]), await Promise.all([r.set([-125, 140]), f.set([125, -140])]), await Promise.all([r.set([-125, 0]), f.set([125, -0])]), await Promise.all([r.set([125, 0]), f.set([-125, 0])]);
  }
  async function u() {
    await s(), a || u();
  }
  async function _() {
    await Promise.all([r.set([125, 0]), f.set([-125, 0])]), u();
  }
  return ca(() => (_(), () => a = !0)), n.$$set = (c) => {
    "margin" in c && t(0, o = c.margin);
  }, [o, l, i, r, f];
}
class Wl extends sa {
  constructor(e) {
    super(), fa(this, e, ma, da, _a, { margin: 0 });
  }
}
const {
  SvelteComponent: ha,
  append: Ve,
  attr: _e,
  binding_callbacks: Pn,
  check_outros: sn,
  create_component: Ul,
  create_slot: Zl,
  destroy_component: Hl,
  destroy_each: Gl,
  detach: E,
  element: ve,
  empty: $e,
  ensure_array_like: kt,
  get_all_dirty_from_scope: Xl,
  get_slot_changes: Yl,
  group_outros: an,
  init: ba,
  insert: z,
  mount_component: Kl,
  noop: rn,
  safe_not_equal: ga,
  set_data: le,
  set_style: Ne,
  space: ne,
  text: F,
  toggle_class: ee,
  transition_in: ue,
  transition_out: ye,
  update_slot_base: Jl
} = window.__gradio__svelte__internal, { tick: wa } = window.__gradio__svelte__internal, { onDestroy: ka } = window.__gradio__svelte__internal, { createEventDispatcher: pa } = window.__gradio__svelte__internal, va = (n) => ({}), On = (n) => ({}), ya = (n) => ({}), Wn = (n) => ({});
function Un(n, e, t) {
  const l = n.slice();
  return l[40] = e[t], l[42] = t, l;
}
function Zn(n, e, t) {
  const l = n.slice();
  return l[40] = e[t], l;
}
function Ca(n) {
  let e, t, l, i, o = (
    /*i18n*/
    n[1]("common.error") + ""
  ), r, f, a;
  t = new ze({
    props: {
      Icon: Bl,
      label: (
        /*i18n*/
        n[1]("common.clear")
      ),
      disabled: !1
    }
  }), t.$on(
    "click",
    /*click_handler*/
    n[32]
  );
  const s = (
    /*#slots*/
    n[30].error
  ), u = Zl(
    s,
    n,
    /*$$scope*/
    n[29],
    On
  );
  return {
    c() {
      e = ve("div"), Ul(t.$$.fragment), l = ne(), i = ve("span"), r = F(o), f = ne(), u && u.c(), _e(e, "class", "clear-status svelte-16nch4a"), _e(i, "class", "error svelte-16nch4a");
    },
    m(_, c) {
      z(_, e, c), Kl(t, e, null), z(_, l, c), z(_, i, c), Ve(i, r), z(_, f, c), u && u.m(_, c), a = !0;
    },
    p(_, c) {
      const d = {};
      c[0] & /*i18n*/
      2 && (d.label = /*i18n*/
      _[1]("common.clear")), t.$set(d), (!a || c[0] & /*i18n*/
      2) && o !== (o = /*i18n*/
      _[1]("common.error") + "") && le(r, o), u && u.p && (!a || c[0] & /*$$scope*/
      536870912) && Jl(
        u,
        s,
        _,
        /*$$scope*/
        _[29],
        a ? Yl(
          s,
          /*$$scope*/
          _[29],
          c,
          va
        ) : Xl(
          /*$$scope*/
          _[29]
        ),
        On
      );
    },
    i(_) {
      a || (ue(t.$$.fragment, _), ue(u, _), a = !0);
    },
    o(_) {
      ye(t.$$.fragment, _), ye(u, _), a = !1;
    },
    d(_) {
      _ && (E(e), E(l), E(i), E(f)), Hl(t), u && u.d(_);
    }
  };
}
function qa(n) {
  let e, t, l, i, o, r, f, a, s, u = (
    /*variant*/
    n[8] === "default" && /*show_eta_bar*/
    n[18] && /*show_progress*/
    n[6] === "full" && Hn(n)
  );
  function _(p, b) {
    if (
      /*progress*/
      p[7]
    )
      return Ea;
    if (
      /*queue_position*/
      p[2] !== null && /*queue_size*/
      p[3] !== void 0 && /*queue_position*/
      p[2] >= 0
    )
      return La;
    if (
      /*queue_position*/
      p[2] === 0
    )
      return Sa;
  }
  let c = _(n), d = c && c(n), h = (
    /*timer*/
    n[5] && Yn(n)
  );
  const y = [Ma, Ia], S = [];
  function v(p, b) {
    return (
      /*last_progress_level*/
      p[15] != null ? 0 : (
        /*show_progress*/
        p[6] === "full" ? 1 : -1
      )
    );
  }
  ~(o = v(n)) && (r = S[o] = y[o](n));
  let k = !/*timer*/
  n[5] && tl(n);
  return {
    c() {
      u && u.c(), e = ne(), t = ve("div"), d && d.c(), l = ne(), h && h.c(), i = ne(), r && r.c(), f = ne(), k && k.c(), a = $e(), _e(t, "class", "progress-text svelte-16nch4a"), ee(
        t,
        "meta-text-center",
        /*variant*/
        n[8] === "center"
      ), ee(
        t,
        "meta-text",
        /*variant*/
        n[8] === "default"
      );
    },
    m(p, b) {
      u && u.m(p, b), z(p, e, b), z(p, t, b), d && d.m(t, null), Ve(t, l), h && h.m(t, null), z(p, i, b), ~o && S[o].m(p, b), z(p, f, b), k && k.m(p, b), z(p, a, b), s = !0;
    },
    p(p, b) {
      /*variant*/
      p[8] === "default" && /*show_eta_bar*/
      p[18] && /*show_progress*/
      p[6] === "full" ? u ? u.p(p, b) : (u = Hn(p), u.c(), u.m(e.parentNode, e)) : u && (u.d(1), u = null), c === (c = _(p)) && d ? d.p(p, b) : (d && d.d(1), d = c && c(p), d && (d.c(), d.m(t, l))), /*timer*/
      p[5] ? h ? h.p(p, b) : (h = Yn(p), h.c(), h.m(t, null)) : h && (h.d(1), h = null), (!s || b[0] & /*variant*/
      256) && ee(
        t,
        "meta-text-center",
        /*variant*/
        p[8] === "center"
      ), (!s || b[0] & /*variant*/
      256) && ee(
        t,
        "meta-text",
        /*variant*/
        p[8] === "default"
      );
      let q = o;
      o = v(p), o === q ? ~o && S[o].p(p, b) : (r && (an(), ye(S[q], 1, 1, () => {
        S[q] = null;
      }), sn()), ~o ? (r = S[o], r ? r.p(p, b) : (r = S[o] = y[o](p), r.c()), ue(r, 1), r.m(f.parentNode, f)) : r = null), /*timer*/
      p[5] ? k && (an(), ye(k, 1, 1, () => {
        k = null;
      }), sn()) : k ? (k.p(p, b), b[0] & /*timer*/
      32 && ue(k, 1)) : (k = tl(p), k.c(), ue(k, 1), k.m(a.parentNode, a));
    },
    i(p) {
      s || (ue(r), ue(k), s = !0);
    },
    o(p) {
      ye(r), ye(k), s = !1;
    },
    d(p) {
      p && (E(e), E(t), E(i), E(f), E(a)), u && u.d(p), d && d.d(), h && h.d(), ~o && S[o].d(p), k && k.d(p);
    }
  };
}
function Hn(n) {
  let e, t = `translateX(${/*eta_level*/
  (n[17] || 0) * 100 - 100}%)`;
  return {
    c() {
      e = ve("div"), _e(e, "class", "eta-bar svelte-16nch4a"), Ne(e, "transform", t);
    },
    m(l, i) {
      z(l, e, i);
    },
    p(l, i) {
      i[0] & /*eta_level*/
      131072 && t !== (t = `translateX(${/*eta_level*/
      (l[17] || 0) * 100 - 100}%)`) && Ne(e, "transform", t);
    },
    d(l) {
      l && E(e);
    }
  };
}
function Sa(n) {
  let e;
  return {
    c() {
      e = F("processing |");
    },
    m(t, l) {
      z(t, e, l);
    },
    p: rn,
    d(t) {
      t && E(e);
    }
  };
}
function La(n) {
  let e, t = (
    /*queue_position*/
    n[2] + 1 + ""
  ), l, i, o, r;
  return {
    c() {
      e = F("queue: "), l = F(t), i = F("/"), o = F(
        /*queue_size*/
        n[3]
      ), r = F(" |");
    },
    m(f, a) {
      z(f, e, a), z(f, l, a), z(f, i, a), z(f, o, a), z(f, r, a);
    },
    p(f, a) {
      a[0] & /*queue_position*/
      4 && t !== (t = /*queue_position*/
      f[2] + 1 + "") && le(l, t), a[0] & /*queue_size*/
      8 && le(
        o,
        /*queue_size*/
        f[3]
      );
    },
    d(f) {
      f && (E(e), E(l), E(i), E(o), E(r));
    }
  };
}
function Ea(n) {
  let e, t = kt(
    /*progress*/
    n[7]
  ), l = [];
  for (let i = 0; i < t.length; i += 1)
    l[i] = Xn(Zn(n, t, i));
  return {
    c() {
      for (let i = 0; i < l.length; i += 1)
        l[i].c();
      e = $e();
    },
    m(i, o) {
      for (let r = 0; r < l.length; r += 1)
        l[r] && l[r].m(i, o);
      z(i, e, o);
    },
    p(i, o) {
      if (o[0] & /*progress*/
      128) {
        t = kt(
          /*progress*/
          i[7]
        );
        let r;
        for (r = 0; r < t.length; r += 1) {
          const f = Zn(i, t, r);
          l[r] ? l[r].p(f, o) : (l[r] = Xn(f), l[r].c(), l[r].m(e.parentNode, e));
        }
        for (; r < l.length; r += 1)
          l[r].d(1);
        l.length = t.length;
      }
    },
    d(i) {
      i && E(e), Gl(l, i);
    }
  };
}
function Gn(n) {
  let e, t = (
    /*p*/
    n[40].unit + ""
  ), l, i, o = " ", r;
  function f(u, _) {
    return (
      /*p*/
      u[40].length != null ? ja : za
    );
  }
  let a = f(n), s = a(n);
  return {
    c() {
      s.c(), e = ne(), l = F(t), i = F(" | "), r = F(o);
    },
    m(u, _) {
      s.m(u, _), z(u, e, _), z(u, l, _), z(u, i, _), z(u, r, _);
    },
    p(u, _) {
      a === (a = f(u)) && s ? s.p(u, _) : (s.d(1), s = a(u), s && (s.c(), s.m(e.parentNode, e))), _[0] & /*progress*/
      128 && t !== (t = /*p*/
      u[40].unit + "") && le(l, t);
    },
    d(u) {
      u && (E(e), E(l), E(i), E(r)), s.d(u);
    }
  };
}
function za(n) {
  let e = Ke(
    /*p*/
    n[40].index || 0
  ) + "", t;
  return {
    c() {
      t = F(e);
    },
    m(l, i) {
      z(l, t, i);
    },
    p(l, i) {
      i[0] & /*progress*/
      128 && e !== (e = Ke(
        /*p*/
        l[40].index || 0
      ) + "") && le(t, e);
    },
    d(l) {
      l && E(t);
    }
  };
}
function ja(n) {
  let e = Ke(
    /*p*/
    n[40].index || 0
  ) + "", t, l, i = Ke(
    /*p*/
    n[40].length
  ) + "", o;
  return {
    c() {
      t = F(e), l = F("/"), o = F(i);
    },
    m(r, f) {
      z(r, t, f), z(r, l, f), z(r, o, f);
    },
    p(r, f) {
      f[0] & /*progress*/
      128 && e !== (e = Ke(
        /*p*/
        r[40].index || 0
      ) + "") && le(t, e), f[0] & /*progress*/
      128 && i !== (i = Ke(
        /*p*/
        r[40].length
      ) + "") && le(o, i);
    },
    d(r) {
      r && (E(t), E(l), E(o));
    }
  };
}
function Xn(n) {
  let e, t = (
    /*p*/
    n[40].index != null && Gn(n)
  );
  return {
    c() {
      t && t.c(), e = $e();
    },
    m(l, i) {
      t && t.m(l, i), z(l, e, i);
    },
    p(l, i) {
      /*p*/
      l[40].index != null ? t ? t.p(l, i) : (t = Gn(l), t.c(), t.m(e.parentNode, e)) : t && (t.d(1), t = null);
    },
    d(l) {
      l && E(e), t && t.d(l);
    }
  };
}
function Yn(n) {
  let e, t = (
    /*eta*/
    n[0] ? `/${/*formatted_eta*/
    n[19]}` : ""
  ), l, i;
  return {
    c() {
      e = F(
        /*formatted_timer*/
        n[20]
      ), l = F(t), i = F("s");
    },
    m(o, r) {
      z(o, e, r), z(o, l, r), z(o, i, r);
    },
    p(o, r) {
      r[0] & /*formatted_timer*/
      1048576 && le(
        e,
        /*formatted_timer*/
        o[20]
      ), r[0] & /*eta, formatted_eta*/
      524289 && t !== (t = /*eta*/
      o[0] ? `/${/*formatted_eta*/
      o[19]}` : "") && le(l, t);
    },
    d(o) {
      o && (E(e), E(l), E(i));
    }
  };
}
function Ia(n) {
  let e, t;
  return e = new Wl({
    props: { margin: (
      /*variant*/
      n[8] === "default"
    ) }
  }), {
    c() {
      Ul(e.$$.fragment);
    },
    m(l, i) {
      Kl(e, l, i), t = !0;
    },
    p(l, i) {
      const o = {};
      i[0] & /*variant*/
      256 && (o.margin = /*variant*/
      l[8] === "default"), e.$set(o);
    },
    i(l) {
      t || (ue(e.$$.fragment, l), t = !0);
    },
    o(l) {
      ye(e.$$.fragment, l), t = !1;
    },
    d(l) {
      Hl(e, l);
    }
  };
}
function Ma(n) {
  let e, t, l, i, o, r = `${/*last_progress_level*/
  n[15] * 100}%`, f = (
    /*progress*/
    n[7] != null && Kn(n)
  );
  return {
    c() {
      e = ve("div"), t = ve("div"), f && f.c(), l = ne(), i = ve("div"), o = ve("div"), _e(t, "class", "progress-level-inner svelte-16nch4a"), _e(o, "class", "progress-bar svelte-16nch4a"), Ne(o, "width", r), _e(i, "class", "progress-bar-wrap svelte-16nch4a"), _e(e, "class", "progress-level svelte-16nch4a");
    },
    m(a, s) {
      z(a, e, s), Ve(e, t), f && f.m(t, null), Ve(e, l), Ve(e, i), Ve(i, o), n[31](o);
    },
    p(a, s) {
      /*progress*/
      a[7] != null ? f ? f.p(a, s) : (f = Kn(a), f.c(), f.m(t, null)) : f && (f.d(1), f = null), s[0] & /*last_progress_level*/
      32768 && r !== (r = `${/*last_progress_level*/
      a[15] * 100}%`) && Ne(o, "width", r);
    },
    i: rn,
    o: rn,
    d(a) {
      a && E(e), f && f.d(), n[31](null);
    }
  };
}
function Kn(n) {
  let e, t = kt(
    /*progress*/
    n[7]
  ), l = [];
  for (let i = 0; i < t.length; i += 1)
    l[i] = el(Un(n, t, i));
  return {
    c() {
      for (let i = 0; i < l.length; i += 1)
        l[i].c();
      e = $e();
    },
    m(i, o) {
      for (let r = 0; r < l.length; r += 1)
        l[r] && l[r].m(i, o);
      z(i, e, o);
    },
    p(i, o) {
      if (o[0] & /*progress_level, progress*/
      16512) {
        t = kt(
          /*progress*/
          i[7]
        );
        let r;
        for (r = 0; r < t.length; r += 1) {
          const f = Un(i, t, r);
          l[r] ? l[r].p(f, o) : (l[r] = el(f), l[r].c(), l[r].m(e.parentNode, e));
        }
        for (; r < l.length; r += 1)
          l[r].d(1);
        l.length = t.length;
      }
    },
    d(i) {
      i && E(e), Gl(l, i);
    }
  };
}
function Jn(n) {
  let e, t, l, i, o = (
    /*i*/
    n[42] !== 0 && Aa()
  ), r = (
    /*p*/
    n[40].desc != null && Qn(n)
  ), f = (
    /*p*/
    n[40].desc != null && /*progress_level*/
    n[14] && /*progress_level*/
    n[14][
      /*i*/
      n[42]
    ] != null && xn()
  ), a = (
    /*progress_level*/
    n[14] != null && $n(n)
  );
  return {
    c() {
      o && o.c(), e = ne(), r && r.c(), t = ne(), f && f.c(), l = ne(), a && a.c(), i = $e();
    },
    m(s, u) {
      o && o.m(s, u), z(s, e, u), r && r.m(s, u), z(s, t, u), f && f.m(s, u), z(s, l, u), a && a.m(s, u), z(s, i, u);
    },
    p(s, u) {
      /*p*/
      s[40].desc != null ? r ? r.p(s, u) : (r = Qn(s), r.c(), r.m(t.parentNode, t)) : r && (r.d(1), r = null), /*p*/
      s[40].desc != null && /*progress_level*/
      s[14] && /*progress_level*/
      s[14][
        /*i*/
        s[42]
      ] != null ? f || (f = xn(), f.c(), f.m(l.parentNode, l)) : f && (f.d(1), f = null), /*progress_level*/
      s[14] != null ? a ? a.p(s, u) : (a = $n(s), a.c(), a.m(i.parentNode, i)) : a && (a.d(1), a = null);
    },
    d(s) {
      s && (E(e), E(t), E(l), E(i)), o && o.d(s), r && r.d(s), f && f.d(s), a && a.d(s);
    }
  };
}
function Aa(n) {
  let e;
  return {
    c() {
      e = F(" /");
    },
    m(t, l) {
      z(t, e, l);
    },
    d(t) {
      t && E(e);
    }
  };
}
function Qn(n) {
  let e = (
    /*p*/
    n[40].desc + ""
  ), t;
  return {
    c() {
      t = F(e);
    },
    m(l, i) {
      z(l, t, i);
    },
    p(l, i) {
      i[0] & /*progress*/
      128 && e !== (e = /*p*/
      l[40].desc + "") && le(t, e);
    },
    d(l) {
      l && E(t);
    }
  };
}
function xn(n) {
  let e;
  return {
    c() {
      e = F("-");
    },
    m(t, l) {
      z(t, e, l);
    },
    d(t) {
      t && E(e);
    }
  };
}
function $n(n) {
  let e = (100 * /*progress_level*/
  (n[14][
    /*i*/
    n[42]
  ] || 0)).toFixed(1) + "", t, l;
  return {
    c() {
      t = F(e), l = F("%");
    },
    m(i, o) {
      z(i, t, o), z(i, l, o);
    },
    p(i, o) {
      o[0] & /*progress_level*/
      16384 && e !== (e = (100 * /*progress_level*/
      (i[14][
        /*i*/
        i[42]
      ] || 0)).toFixed(1) + "") && le(t, e);
    },
    d(i) {
      i && (E(t), E(l));
    }
  };
}
function el(n) {
  let e, t = (
    /*p*/
    (n[40].desc != null || /*progress_level*/
    n[14] && /*progress_level*/
    n[14][
      /*i*/
      n[42]
    ] != null) && Jn(n)
  );
  return {
    c() {
      t && t.c(), e = $e();
    },
    m(l, i) {
      t && t.m(l, i), z(l, e, i);
    },
    p(l, i) {
      /*p*/
      l[40].desc != null || /*progress_level*/
      l[14] && /*progress_level*/
      l[14][
        /*i*/
        l[42]
      ] != null ? t ? t.p(l, i) : (t = Jn(l), t.c(), t.m(e.parentNode, e)) : t && (t.d(1), t = null);
    },
    d(l) {
      l && E(e), t && t.d(l);
    }
  };
}
function tl(n) {
  let e, t, l, i;
  const o = (
    /*#slots*/
    n[30]["additional-loading-text"]
  ), r = Zl(
    o,
    n,
    /*$$scope*/
    n[29],
    Wn
  );
  return {
    c() {
      e = ve("p"), t = F(
        /*loading_text*/
        n[9]
      ), l = ne(), r && r.c(), _e(e, "class", "loading svelte-16nch4a");
    },
    m(f, a) {
      z(f, e, a), Ve(e, t), z(f, l, a), r && r.m(f, a), i = !0;
    },
    p(f, a) {
      (!i || a[0] & /*loading_text*/
      512) && le(
        t,
        /*loading_text*/
        f[9]
      ), r && r.p && (!i || a[0] & /*$$scope*/
      536870912) && Jl(
        r,
        o,
        f,
        /*$$scope*/
        f[29],
        i ? Yl(
          o,
          /*$$scope*/
          f[29],
          a,
          ya
        ) : Xl(
          /*$$scope*/
          f[29]
        ),
        Wn
      );
    },
    i(f) {
      i || (ue(r, f), i = !0);
    },
    o(f) {
      ye(r, f), i = !1;
    },
    d(f) {
      f && (E(e), E(l)), r && r.d(f);
    }
  };
}
function Ra(n) {
  let e, t, l, i, o;
  const r = [qa, Ca], f = [];
  function a(s, u) {
    return (
      /*status*/
      s[4] === "pending" ? 0 : (
        /*status*/
        s[4] === "error" ? 1 : -1
      )
    );
  }
  return ~(t = a(n)) && (l = f[t] = r[t](n)), {
    c() {
      e = ve("div"), l && l.c(), _e(e, "class", i = "wrap " + /*variant*/
      n[8] + " " + /*show_progress*/
      n[6] + " svelte-16nch4a"), ee(e, "hide", !/*status*/
      n[4] || /*status*/
      n[4] === "complete" || /*show_progress*/
      n[6] === "hidden"), ee(
        e,
        "translucent",
        /*variant*/
        n[8] === "center" && /*status*/
        (n[4] === "pending" || /*status*/
        n[4] === "error") || /*translucent*/
        n[11] || /*show_progress*/
        n[6] === "minimal"
      ), ee(
        e,
        "generating",
        /*status*/
        n[4] === "generating"
      ), ee(
        e,
        "border",
        /*border*/
        n[12]
      ), Ne(
        e,
        "position",
        /*absolute*/
        n[10] ? "absolute" : "static"
      ), Ne(
        e,
        "padding",
        /*absolute*/
        n[10] ? "0" : "var(--size-8) 0"
      );
    },
    m(s, u) {
      z(s, e, u), ~t && f[t].m(e, null), n[33](e), o = !0;
    },
    p(s, u) {
      let _ = t;
      t = a(s), t === _ ? ~t && f[t].p(s, u) : (l && (an(), ye(f[_], 1, 1, () => {
        f[_] = null;
      }), sn()), ~t ? (l = f[t], l ? l.p(s, u) : (l = f[t] = r[t](s), l.c()), ue(l, 1), l.m(e, null)) : l = null), (!o || u[0] & /*variant, show_progress*/
      320 && i !== (i = "wrap " + /*variant*/
      s[8] + " " + /*show_progress*/
      s[6] + " svelte-16nch4a")) && _e(e, "class", i), (!o || u[0] & /*variant, show_progress, status, show_progress*/
      336) && ee(e, "hide", !/*status*/
      s[4] || /*status*/
      s[4] === "complete" || /*show_progress*/
      s[6] === "hidden"), (!o || u[0] & /*variant, show_progress, variant, status, translucent, show_progress*/
      2384) && ee(
        e,
        "translucent",
        /*variant*/
        s[8] === "center" && /*status*/
        (s[4] === "pending" || /*status*/
        s[4] === "error") || /*translucent*/
        s[11] || /*show_progress*/
        s[6] === "minimal"
      ), (!o || u[0] & /*variant, show_progress, status*/
      336) && ee(
        e,
        "generating",
        /*status*/
        s[4] === "generating"
      ), (!o || u[0] & /*variant, show_progress, border*/
      4416) && ee(
        e,
        "border",
        /*border*/
        s[12]
      ), u[0] & /*absolute*/
      1024 && Ne(
        e,
        "position",
        /*absolute*/
        s[10] ? "absolute" : "static"
      ), u[0] & /*absolute*/
      1024 && Ne(
        e,
        "padding",
        /*absolute*/
        s[10] ? "0" : "var(--size-8) 0"
      );
    },
    i(s) {
      o || (ue(l), o = !0);
    },
    o(s) {
      ye(l), o = !1;
    },
    d(s) {
      s && E(e), ~t && f[t].d(), n[33](null);
    }
  };
}
let ht = [], Xt = !1;
async function Da(n, e = !0) {
  if (!(window.__gradio_mode__ === "website" || window.__gradio_mode__ !== "app" && e !== !0)) {
    if (ht.push(n), !Xt)
      Xt = !0;
    else
      return;
    await wa(), requestAnimationFrame(() => {
      let t = [0, 0];
      for (let l = 0; l < ht.length; l++) {
        const o = ht[l].getBoundingClientRect();
        (l === 0 || o.top + window.scrollY <= t[0]) && (t[0] = o.top + window.scrollY, t[1] = l);
      }
      window.scrollTo({ top: t[0] - 20, behavior: "smooth" }), Xt = !1, ht = [];
    });
  }
}
function Fa(n, e, t) {
  let l, { $$slots: i = {}, $$scope: o } = e;
  const r = pa();
  let { i18n: f } = e, { eta: a = null } = e, { queue_position: s } = e, { queue_size: u } = e, { status: _ } = e, { scroll_to_output: c = !1 } = e, { timer: d = !0 } = e, { show_progress: h = "full" } = e, { message: y = null } = e, { progress: S = null } = e, { variant: v = "default" } = e, { loading_text: k = "Loading..." } = e, { absolute: p = !0 } = e, { translucent: b = !1 } = e, { border: q = !1 } = e, { autoscroll: g } = e, L, C = !1, P = 0, A = 0, O = null, B = null, me = 0, Z = null, he, H = null, ie = !0;
  const qe = () => {
    t(0, a = t(27, O = t(19, be = null))), t(25, P = performance.now()), t(26, A = 0), C = !0, Q();
  };
  function Q() {
    requestAnimationFrame(() => {
      t(26, A = (performance.now() - P) / 1e3), C && Q();
    });
  }
  function N() {
    t(26, A = 0), t(0, a = t(27, O = t(19, be = null))), C && (C = !1);
  }
  ka(() => {
    C && N();
  });
  let be = null;
  function Te(m) {
    Pn[m ? "unshift" : "push"](() => {
      H = m, t(16, H), t(7, S), t(14, Z), t(15, he);
    });
  }
  const He = () => {
    r("clear_status");
  };
  function et(m) {
    Pn[m ? "unshift" : "push"](() => {
      L = m, t(13, L);
    });
  }
  return n.$$set = (m) => {
    "i18n" in m && t(1, f = m.i18n), "eta" in m && t(0, a = m.eta), "queue_position" in m && t(2, s = m.queue_position), "queue_size" in m && t(3, u = m.queue_size), "status" in m && t(4, _ = m.status), "scroll_to_output" in m && t(22, c = m.scroll_to_output), "timer" in m && t(5, d = m.timer), "show_progress" in m && t(6, h = m.show_progress), "message" in m && t(23, y = m.message), "progress" in m && t(7, S = m.progress), "variant" in m && t(8, v = m.variant), "loading_text" in m && t(9, k = m.loading_text), "absolute" in m && t(10, p = m.absolute), "translucent" in m && t(11, b = m.translucent), "border" in m && t(12, q = m.border), "autoscroll" in m && t(24, g = m.autoscroll), "$$scope" in m && t(29, o = m.$$scope);
  }, n.$$.update = () => {
    n.$$.dirty[0] & /*eta, old_eta, timer_start, eta_from_start*/
    436207617 && (a === null && t(0, a = O), a != null && O !== a && (t(28, B = (performance.now() - P) / 1e3 + a), t(19, be = B.toFixed(1)), t(27, O = a))), n.$$.dirty[0] & /*eta_from_start, timer_diff*/
    335544320 && t(17, me = B === null || B <= 0 || !A ? null : Math.min(A / B, 1)), n.$$.dirty[0] & /*progress*/
    128 && S != null && t(18, ie = !1), n.$$.dirty[0] & /*progress, progress_level, progress_bar, last_progress_level*/
    114816 && (S != null ? t(14, Z = S.map((m) => {
      if (m.index != null && m.length != null)
        return m.index / m.length;
      if (m.progress != null)
        return m.progress;
    })) : t(14, Z = null), Z ? (t(15, he = Z[Z.length - 1]), H && (he === 0 ? t(16, H.style.transition = "0", H) : t(16, H.style.transition = "150ms", H))) : t(15, he = void 0)), n.$$.dirty[0] & /*status*/
    16 && (_ === "pending" ? qe() : N()), n.$$.dirty[0] & /*el, scroll_to_output, status, autoscroll*/
    20979728 && L && c && (_ === "pending" || _ === "complete") && Da(L, g), n.$$.dirty[0] & /*status, message*/
    8388624, n.$$.dirty[0] & /*timer_diff*/
    67108864 && t(20, l = A.toFixed(1));
  }, [
    a,
    f,
    s,
    u,
    _,
    d,
    h,
    S,
    v,
    k,
    p,
    b,
    q,
    L,
    Z,
    he,
    H,
    me,
    ie,
    be,
    l,
    r,
    c,
    y,
    g,
    P,
    A,
    O,
    B,
    o,
    i,
    Te,
    He,
    et
  ];
}
class Ba extends ha {
  constructor(e) {
    super(), ba(
      this,
      e,
      Fa,
      Ra,
      ga,
      {
        i18n: 1,
        eta: 0,
        queue_position: 2,
        queue_size: 3,
        status: 4,
        scroll_to_output: 22,
        timer: 5,
        show_progress: 6,
        message: 23,
        progress: 7,
        variant: 8,
        loading_text: 9,
        absolute: 10,
        translucent: 11,
        border: 12,
        autoscroll: 24
      },
      null,
      [-1, -1]
    );
  }
}
const {
  SvelteComponent: Na,
  append: Ql,
  attr: R,
  bubble: Ta,
  check_outros: Va,
  create_slot: xl,
  detach: st,
  element: jt,
  empty: Pa,
  get_all_dirty_from_scope: $l,
  get_slot_changes: ei,
  group_outros: Oa,
  init: Wa,
  insert: at,
  listen: Ua,
  safe_not_equal: Za,
  set_style: J,
  space: ti,
  src_url_equal: pt,
  toggle_class: Je,
  transition_in: vt,
  transition_out: yt,
  update_slot_base: ni
} = window.__gradio__svelte__internal;
function Ha(n) {
  let e, t, l, i, o, r, f = (
    /*icon*/
    n[7] && nl(n)
  );
  const a = (
    /*#slots*/
    n[12].default
  ), s = xl(
    a,
    n,
    /*$$scope*/
    n[11],
    null
  );
  return {
    c() {
      e = jt("button"), f && f.c(), t = ti(), s && s.c(), R(e, "class", l = /*size*/
      n[4] + " " + /*variant*/
      n[3] + " " + /*elem_classes*/
      n[1].join(" ") + " svelte-8huxfn"), R(
        e,
        "id",
        /*elem_id*/
        n[0]
      ), e.disabled = /*disabled*/
      n[8], Je(e, "hidden", !/*visible*/
      n[2]), J(
        e,
        "flex-grow",
        /*scale*/
        n[9]
      ), J(
        e,
        "width",
        /*scale*/
        n[9] === 0 ? "fit-content" : null
      ), J(e, "min-width", typeof /*min_width*/
      n[10] == "number" ? `calc(min(${/*min_width*/
      n[10]}px, 100%))` : null);
    },
    m(u, _) {
      at(u, e, _), f && f.m(e, null), Ql(e, t), s && s.m(e, null), i = !0, o || (r = Ua(
        e,
        "click",
        /*click_handler*/
        n[13]
      ), o = !0);
    },
    p(u, _) {
      /*icon*/
      u[7] ? f ? f.p(u, _) : (f = nl(u), f.c(), f.m(e, t)) : f && (f.d(1), f = null), s && s.p && (!i || _ & /*$$scope*/
      2048) && ni(
        s,
        a,
        u,
        /*$$scope*/
        u[11],
        i ? ei(
          a,
          /*$$scope*/
          u[11],
          _,
          null
        ) : $l(
          /*$$scope*/
          u[11]
        ),
        null
      ), (!i || _ & /*size, variant, elem_classes*/
      26 && l !== (l = /*size*/
      u[4] + " " + /*variant*/
      u[3] + " " + /*elem_classes*/
      u[1].join(" ") + " svelte-8huxfn")) && R(e, "class", l), (!i || _ & /*elem_id*/
      1) && R(
        e,
        "id",
        /*elem_id*/
        u[0]
      ), (!i || _ & /*disabled*/
      256) && (e.disabled = /*disabled*/
      u[8]), (!i || _ & /*size, variant, elem_classes, visible*/
      30) && Je(e, "hidden", !/*visible*/
      u[2]), _ & /*scale*/
      512 && J(
        e,
        "flex-grow",
        /*scale*/
        u[9]
      ), _ & /*scale*/
      512 && J(
        e,
        "width",
        /*scale*/
        u[9] === 0 ? "fit-content" : null
      ), _ & /*min_width*/
      1024 && J(e, "min-width", typeof /*min_width*/
      u[10] == "number" ? `calc(min(${/*min_width*/
      u[10]}px, 100%))` : null);
    },
    i(u) {
      i || (vt(s, u), i = !0);
    },
    o(u) {
      yt(s, u), i = !1;
    },
    d(u) {
      u && st(e), f && f.d(), s && s.d(u), o = !1, r();
    }
  };
}
function Ga(n) {
  let e, t, l, i, o = (
    /*icon*/
    n[7] && ll(n)
  );
  const r = (
    /*#slots*/
    n[12].default
  ), f = xl(
    r,
    n,
    /*$$scope*/
    n[11],
    null
  );
  return {
    c() {
      e = jt("a"), o && o.c(), t = ti(), f && f.c(), R(
        e,
        "href",
        /*link*/
        n[6]
      ), R(e, "rel", "noopener noreferrer"), R(
        e,
        "aria-disabled",
        /*disabled*/
        n[8]
      ), R(e, "class", l = /*size*/
      n[4] + " " + /*variant*/
      n[3] + " " + /*elem_classes*/
      n[1].join(" ") + " svelte-8huxfn"), R(
        e,
        "id",
        /*elem_id*/
        n[0]
      ), Je(e, "hidden", !/*visible*/
      n[2]), Je(
        e,
        "disabled",
        /*disabled*/
        n[8]
      ), J(
        e,
        "flex-grow",
        /*scale*/
        n[9]
      ), J(
        e,
        "pointer-events",
        /*disabled*/
        n[8] ? "none" : null
      ), J(
        e,
        "width",
        /*scale*/
        n[9] === 0 ? "fit-content" : null
      ), J(e, "min-width", typeof /*min_width*/
      n[10] == "number" ? `calc(min(${/*min_width*/
      n[10]}px, 100%))` : null);
    },
    m(a, s) {
      at(a, e, s), o && o.m(e, null), Ql(e, t), f && f.m(e, null), i = !0;
    },
    p(a, s) {
      /*icon*/
      a[7] ? o ? o.p(a, s) : (o = ll(a), o.c(), o.m(e, t)) : o && (o.d(1), o = null), f && f.p && (!i || s & /*$$scope*/
      2048) && ni(
        f,
        r,
        a,
        /*$$scope*/
        a[11],
        i ? ei(
          r,
          /*$$scope*/
          a[11],
          s,
          null
        ) : $l(
          /*$$scope*/
          a[11]
        ),
        null
      ), (!i || s & /*link*/
      64) && R(
        e,
        "href",
        /*link*/
        a[6]
      ), (!i || s & /*disabled*/
      256) && R(
        e,
        "aria-disabled",
        /*disabled*/
        a[8]
      ), (!i || s & /*size, variant, elem_classes*/
      26 && l !== (l = /*size*/
      a[4] + " " + /*variant*/
      a[3] + " " + /*elem_classes*/
      a[1].join(" ") + " svelte-8huxfn")) && R(e, "class", l), (!i || s & /*elem_id*/
      1) && R(
        e,
        "id",
        /*elem_id*/
        a[0]
      ), (!i || s & /*size, variant, elem_classes, visible*/
      30) && Je(e, "hidden", !/*visible*/
      a[2]), (!i || s & /*size, variant, elem_classes, disabled*/
      282) && Je(
        e,
        "disabled",
        /*disabled*/
        a[8]
      ), s & /*scale*/
      512 && J(
        e,
        "flex-grow",
        /*scale*/
        a[9]
      ), s & /*disabled*/
      256 && J(
        e,
        "pointer-events",
        /*disabled*/
        a[8] ? "none" : null
      ), s & /*scale*/
      512 && J(
        e,
        "width",
        /*scale*/
        a[9] === 0 ? "fit-content" : null
      ), s & /*min_width*/
      1024 && J(e, "min-width", typeof /*min_width*/
      a[10] == "number" ? `calc(min(${/*min_width*/
      a[10]}px, 100%))` : null);
    },
    i(a) {
      i || (vt(f, a), i = !0);
    },
    o(a) {
      yt(f, a), i = !1;
    },
    d(a) {
      a && st(e), o && o.d(), f && f.d(a);
    }
  };
}
function nl(n) {
  let e, t, l;
  return {
    c() {
      e = jt("img"), R(e, "class", "button-icon svelte-8huxfn"), pt(e.src, t = /*icon*/
      n[7].url) || R(e, "src", t), R(e, "alt", l = `${/*value*/
      n[5]} icon`);
    },
    m(i, o) {
      at(i, e, o);
    },
    p(i, o) {
      o & /*icon*/
      128 && !pt(e.src, t = /*icon*/
      i[7].url) && R(e, "src", t), o & /*value*/
      32 && l !== (l = `${/*value*/
      i[5]} icon`) && R(e, "alt", l);
    },
    d(i) {
      i && st(e);
    }
  };
}
function ll(n) {
  let e, t, l;
  return {
    c() {
      e = jt("img"), R(e, "class", "button-icon svelte-8huxfn"), pt(e.src, t = /*icon*/
      n[7].url) || R(e, "src", t), R(e, "alt", l = `${/*value*/
      n[5]} icon`);
    },
    m(i, o) {
      at(i, e, o);
    },
    p(i, o) {
      o & /*icon*/
      128 && !pt(e.src, t = /*icon*/
      i[7].url) && R(e, "src", t), o & /*value*/
      32 && l !== (l = `${/*value*/
      i[5]} icon`) && R(e, "alt", l);
    },
    d(i) {
      i && st(e);
    }
  };
}
function Xa(n) {
  let e, t, l, i;
  const o = [Ga, Ha], r = [];
  function f(a, s) {
    return (
      /*link*/
      a[6] && /*link*/
      a[6].length > 0 ? 0 : 1
    );
  }
  return e = f(n), t = r[e] = o[e](n), {
    c() {
      t.c(), l = Pa();
    },
    m(a, s) {
      r[e].m(a, s), at(a, l, s), i = !0;
    },
    p(a, [s]) {
      let u = e;
      e = f(a), e === u ? r[e].p(a, s) : (Oa(), yt(r[u], 1, 1, () => {
        r[u] = null;
      }), Va(), t = r[e], t ? t.p(a, s) : (t = r[e] = o[e](a), t.c()), vt(t, 1), t.m(l.parentNode, l));
    },
    i(a) {
      i || (vt(t), i = !0);
    },
    o(a) {
      yt(t), i = !1;
    },
    d(a) {
      a && st(l), r[e].d(a);
    }
  };
}
function Ya(n, e, t) {
  let { $$slots: l = {}, $$scope: i } = e, { elem_id: o = "" } = e, { elem_classes: r = [] } = e, { visible: f = !0 } = e, { variant: a = "secondary" } = e, { size: s = "lg" } = e, { value: u = null } = e, { link: _ = null } = e, { icon: c = null } = e, { disabled: d = !1 } = e, { scale: h = null } = e, { min_width: y = void 0 } = e;
  function S(v) {
    Ta.call(this, n, v);
  }
  return n.$$set = (v) => {
    "elem_id" in v && t(0, o = v.elem_id), "elem_classes" in v && t(1, r = v.elem_classes), "visible" in v && t(2, f = v.visible), "variant" in v && t(3, a = v.variant), "size" in v && t(4, s = v.size), "value" in v && t(5, u = v.value), "link" in v && t(6, _ = v.link), "icon" in v && t(7, c = v.icon), "disabled" in v && t(8, d = v.disabled), "scale" in v && t(9, h = v.scale), "min_width" in v && t(10, y = v.min_width), "$$scope" in v && t(11, i = v.$$scope);
  }, [
    o,
    r,
    f,
    a,
    s,
    u,
    _,
    c,
    d,
    h,
    y,
    i,
    l,
    S
  ];
}
class Ka extends Na {
  constructor(e) {
    super(), Wa(this, e, Ya, Xa, Za, {
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
var Ja = Object.defineProperty, Qa = (n, e, t) => e in n ? Ja(n, e, { enumerable: !0, configurable: !0, writable: !0, value: t }) : n[e] = t, Se = (n, e, t) => (Qa(n, typeof e != "symbol" ? e + "" : e, t), t), li = (n, e, t) => {
  if (!e.has(n))
    throw TypeError("Cannot " + t);
}, nt = (n, e, t) => (li(n, e, "read from private field"), t ? t.call(n) : e.get(n)), xa = (n, e, t) => {
  if (e.has(n))
    throw TypeError("Cannot add the same private member more than once");
  e instanceof WeakSet ? e.add(n) : e.set(n, t);
}, $a = (n, e, t, l) => (li(n, e, "write to private field"), e.set(n, t), t), Fe;
new Intl.Collator(0, { numeric: 1 }).compare;
class Yt {
  constructor({
    path: e,
    url: t,
    orig_name: l,
    size: i,
    blob: o,
    is_stream: r,
    mime_type: f,
    alt_text: a
  }) {
    Se(this, "path"), Se(this, "url"), Se(this, "orig_name"), Se(this, "size"), Se(this, "blob"), Se(this, "is_stream"), Se(this, "mime_type"), Se(this, "alt_text"), Se(this, "meta", { _type: "gradio.FileData" }), this.path = e, this.url = t, this.orig_name = l, this.size = i, this.blob = t ? void 0 : o, this.is_stream = r, this.mime_type = f, this.alt_text = a;
  }
}
typeof process < "u" && process.versions && process.versions.node;
class $f extends TransformStream {
  /** Constructs a new instance. */
  constructor(e = { allowCR: !1 }) {
    super({
      transform: (t, l) => {
        for (t = nt(this, Fe) + t; ; ) {
          const i = t.indexOf(`
`), o = e.allowCR ? t.indexOf("\r") : -1;
          if (o !== -1 && o !== t.length - 1 && (i === -1 || i - 1 > o)) {
            l.enqueue(t.slice(0, o)), t = t.slice(o + 1);
            continue;
          }
          if (i === -1)
            break;
          const r = t[i - 1] === "\r" ? i - 1 : i;
          l.enqueue(t.slice(0, r)), t = t.slice(i + 1);
        }
        $a(this, Fe, t);
      },
      flush: (t) => {
        if (nt(this, Fe) === "")
          return;
        const l = e.allowCR && nt(this, Fe).endsWith("\r") ? nt(this, Fe).slice(0, -1) : nt(this, Fe);
        t.enqueue(l);
      }
    }), xa(this, Fe, "");
  }
}
Fe = /* @__PURE__ */ new WeakMap();
const { setContext: eu, getContext: er } = window.__gradio__svelte__internal, tr = "WORKER_PROXY_CONTEXT_KEY";
function nr() {
  return er(tr);
}
function lr(n) {
  return n.host === window.location.host || n.host === "localhost:7860" || n.host === "127.0.0.1:7860" || // Ref: https://github.com/gradio-app/gradio/blob/v3.32.0/js/app/src/Index.svelte#L194
  n.host === "lite.local";
}
function ir(n, e) {
  const t = e.toLowerCase();
  for (const [l, i] of Object.entries(n))
    if (l.toLowerCase() === t)
      return i;
}
function or(n) {
  if (n == null)
    return !1;
  const e = new URL(n, window.location.href);
  return !(!lr(e) || e.protocol !== "http:" && e.protocol !== "https:");
}
const {
  SvelteComponent: sr,
  assign: Ct,
  check_outros: ii,
  compute_rest_props: il,
  create_slot: cn,
  detach: It,
  element: oi,
  empty: si,
  exclude_internal_props: ar,
  get_all_dirty_from_scope: dn,
  get_slot_changes: mn,
  get_spread_update: ai,
  group_outros: ri,
  init: rr,
  insert: Mt,
  listen: fi,
  prevent_default: fr,
  safe_not_equal: ur,
  set_attributes: qt,
  transition_in: Ue,
  transition_out: Ze,
  update_slot_base: hn
} = window.__gradio__svelte__internal, { createEventDispatcher: _r } = window.__gradio__svelte__internal;
function cr(n) {
  let e, t, l, i, o;
  const r = (
    /*#slots*/
    n[8].default
  ), f = cn(
    r,
    n,
    /*$$scope*/
    n[7],
    null
  );
  let a = [
    { href: (
      /*href*/
      n[0]
    ) },
    {
      target: t = typeof window < "u" && window.__is_colab__ ? "_blank" : null
    },
    { rel: "noopener noreferrer" },
    { download: (
      /*download*/
      n[1]
    ) },
    /*$$restProps*/
    n[6]
  ], s = {};
  for (let u = 0; u < a.length; u += 1)
    s = Ct(s, a[u]);
  return {
    c() {
      e = oi("a"), f && f.c(), qt(e, s);
    },
    m(u, _) {
      Mt(u, e, _), f && f.m(e, null), l = !0, i || (o = fi(
        e,
        "click",
        /*dispatch*/
        n[3].bind(null, "click")
      ), i = !0);
    },
    p(u, _) {
      f && f.p && (!l || _ & /*$$scope*/
      128) && hn(
        f,
        r,
        u,
        /*$$scope*/
        u[7],
        l ? mn(
          r,
          /*$$scope*/
          u[7],
          _,
          null
        ) : dn(
          /*$$scope*/
          u[7]
        ),
        null
      ), qt(e, s = ai(a, [
        (!l || _ & /*href*/
        1) && { href: (
          /*href*/
          u[0]
        ) },
        { target: t },
        { rel: "noopener noreferrer" },
        (!l || _ & /*download*/
        2) && { download: (
          /*download*/
          u[1]
        ) },
        _ & /*$$restProps*/
        64 && /*$$restProps*/
        u[6]
      ]));
    },
    i(u) {
      l || (Ue(f, u), l = !0);
    },
    o(u) {
      Ze(f, u), l = !1;
    },
    d(u) {
      u && It(e), f && f.d(u), i = !1, o();
    }
  };
}
function dr(n) {
  let e, t, l, i;
  const o = [hr, mr], r = [];
  function f(a, s) {
    return (
      /*is_downloading*/
      a[2] ? 0 : 1
    );
  }
  return e = f(n), t = r[e] = o[e](n), {
    c() {
      t.c(), l = si();
    },
    m(a, s) {
      r[e].m(a, s), Mt(a, l, s), i = !0;
    },
    p(a, s) {
      let u = e;
      e = f(a), e === u ? r[e].p(a, s) : (ri(), Ze(r[u], 1, 1, () => {
        r[u] = null;
      }), ii(), t = r[e], t ? t.p(a, s) : (t = r[e] = o[e](a), t.c()), Ue(t, 1), t.m(l.parentNode, l));
    },
    i(a) {
      i || (Ue(t), i = !0);
    },
    o(a) {
      Ze(t), i = !1;
    },
    d(a) {
      a && It(l), r[e].d(a);
    }
  };
}
function mr(n) {
  let e, t, l, i;
  const o = (
    /*#slots*/
    n[8].default
  ), r = cn(
    o,
    n,
    /*$$scope*/
    n[7],
    null
  );
  let f = [
    /*$$restProps*/
    n[6],
    { href: (
      /*href*/
      n[0]
    ) }
  ], a = {};
  for (let s = 0; s < f.length; s += 1)
    a = Ct(a, f[s]);
  return {
    c() {
      e = oi("a"), r && r.c(), qt(e, a);
    },
    m(s, u) {
      Mt(s, e, u), r && r.m(e, null), t = !0, l || (i = fi(e, "click", fr(
        /*wasm_click_handler*/
        n[5]
      )), l = !0);
    },
    p(s, u) {
      r && r.p && (!t || u & /*$$scope*/
      128) && hn(
        r,
        o,
        s,
        /*$$scope*/
        s[7],
        t ? mn(
          o,
          /*$$scope*/
          s[7],
          u,
          null
        ) : dn(
          /*$$scope*/
          s[7]
        ),
        null
      ), qt(e, a = ai(f, [
        u & /*$$restProps*/
        64 && /*$$restProps*/
        s[6],
        (!t || u & /*href*/
        1) && { href: (
          /*href*/
          s[0]
        ) }
      ]));
    },
    i(s) {
      t || (Ue(r, s), t = !0);
    },
    o(s) {
      Ze(r, s), t = !1;
    },
    d(s) {
      s && It(e), r && r.d(s), l = !1, i();
    }
  };
}
function hr(n) {
  let e;
  const t = (
    /*#slots*/
    n[8].default
  ), l = cn(
    t,
    n,
    /*$$scope*/
    n[7],
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
      128) && hn(
        l,
        t,
        i,
        /*$$scope*/
        i[7],
        e ? mn(
          t,
          /*$$scope*/
          i[7],
          o,
          null
        ) : dn(
          /*$$scope*/
          i[7]
        ),
        null
      );
    },
    i(i) {
      e || (Ue(l, i), e = !0);
    },
    o(i) {
      Ze(l, i), e = !1;
    },
    d(i) {
      l && l.d(i);
    }
  };
}
function br(n) {
  let e, t, l, i, o;
  const r = [dr, cr], f = [];
  function a(s, u) {
    return u & /*href*/
    1 && (e = null), e == null && (e = !!/*worker_proxy*/
    (s[4] && or(
      /*href*/
      s[0]
    ))), e ? 0 : 1;
  }
  return t = a(n, -1), l = f[t] = r[t](n), {
    c() {
      l.c(), i = si();
    },
    m(s, u) {
      f[t].m(s, u), Mt(s, i, u), o = !0;
    },
    p(s, [u]) {
      let _ = t;
      t = a(s, u), t === _ ? f[t].p(s, u) : (ri(), Ze(f[_], 1, 1, () => {
        f[_] = null;
      }), ii(), l = f[t], l ? l.p(s, u) : (l = f[t] = r[t](s), l.c()), Ue(l, 1), l.m(i.parentNode, i));
    },
    i(s) {
      o || (Ue(l), o = !0);
    },
    o(s) {
      Ze(l), o = !1;
    },
    d(s) {
      s && It(i), f[t].d(s);
    }
  };
}
function gr(n, e, t) {
  const l = ["href", "download"];
  let i = il(e, l), { $$slots: o = {}, $$scope: r } = e;
  var f = this && this.__awaiter || function(h, y, S, v) {
    function k(p) {
      return p instanceof S ? p : new S(function(b) {
        b(p);
      });
    }
    return new (S || (S = Promise))(function(p, b) {
      function q(C) {
        try {
          L(v.next(C));
        } catch (P) {
          b(P);
        }
      }
      function g(C) {
        try {
          L(v.throw(C));
        } catch (P) {
          b(P);
        }
      }
      function L(C) {
        C.done ? p(C.value) : k(C.value).then(q, g);
      }
      L((v = v.apply(h, y || [])).next());
    });
  };
  let { href: a = void 0 } = e, { download: s } = e;
  const u = _r();
  let _ = !1;
  const c = nr();
  function d() {
    return f(this, void 0, void 0, function* () {
      if (_)
        return;
      if (u("click"), a == null)
        throw new Error("href is not defined.");
      if (c == null)
        throw new Error("Wasm worker proxy is not available.");
      const y = new URL(a, window.location.href).pathname;
      t(2, _ = !0), c.httpRequest({
        method: "GET",
        path: y,
        headers: {},
        query_string: ""
      }).then((S) => {
        if (S.status !== 200)
          throw new Error(`Failed to get file ${y} from the Wasm worker.`);
        const v = new Blob(
          [S.body],
          {
            type: ir(S.headers, "content-type")
          }
        ), k = URL.createObjectURL(v), p = document.createElement("a");
        p.href = k, p.download = s, p.click(), URL.revokeObjectURL(k);
      }).finally(() => {
        t(2, _ = !1);
      });
    });
  }
  return n.$$set = (h) => {
    e = Ct(Ct({}, e), ar(h)), t(6, i = il(e, l)), "href" in h && t(0, a = h.href), "download" in h && t(1, s = h.download), "$$scope" in h && t(7, r = h.$$scope);
  }, [
    a,
    s,
    _,
    u,
    c,
    d,
    i,
    r,
    o
  ];
}
class wr extends sr {
  constructor(e) {
    super(), rr(this, e, gr, br, ur, { href: 0, download: 1 });
  }
}
const {
  SvelteComponent: kr,
  append: Kt,
  attr: pr,
  check_outros: Jt,
  create_component: rt,
  destroy_component: ft,
  detach: vr,
  element: yr,
  group_outros: Qt,
  init: Cr,
  insert: qr,
  mount_component: ut,
  safe_not_equal: Sr,
  set_style: ol,
  space: xt,
  toggle_class: sl,
  transition_in: K,
  transition_out: fe
} = window.__gradio__svelte__internal, { createEventDispatcher: Lr } = window.__gradio__svelte__internal;
function al(n) {
  let e, t;
  return e = new ze({
    props: {
      Icon: vs,
      label: (
        /*i18n*/
        n[4]("common.edit")
      )
    }
  }), e.$on(
    "click",
    /*click_handler*/
    n[6]
  ), {
    c() {
      rt(e.$$.fragment);
    },
    m(l, i) {
      ut(e, l, i), t = !0;
    },
    p(l, i) {
      const o = {};
      i & /*i18n*/
      16 && (o.label = /*i18n*/
      l[4]("common.edit")), e.$set(o);
    },
    i(l) {
      t || (K(e.$$.fragment, l), t = !0);
    },
    o(l) {
      fe(e.$$.fragment, l), t = !1;
    },
    d(l) {
      ft(e, l);
    }
  };
}
function rl(n) {
  let e, t;
  return e = new ze({
    props: {
      Icon: Ws,
      label: (
        /*i18n*/
        n[4]("common.undo")
      )
    }
  }), e.$on(
    "click",
    /*click_handler_1*/
    n[7]
  ), {
    c() {
      rt(e.$$.fragment);
    },
    m(l, i) {
      ut(e, l, i), t = !0;
    },
    p(l, i) {
      const o = {};
      i & /*i18n*/
      16 && (o.label = /*i18n*/
      l[4]("common.undo")), e.$set(o);
    },
    i(l) {
      t || (K(e.$$.fragment, l), t = !0);
    },
    o(l) {
      fe(e.$$.fragment, l), t = !1;
    },
    d(l) {
      ft(e, l);
    }
  };
}
function fl(n) {
  let e, t;
  return e = new wr({
    props: {
      href: (
        /*download*/
        n[2]
      ),
      download: !0,
      $$slots: { default: [Er] },
      $$scope: { ctx: n }
    }
  }), {
    c() {
      rt(e.$$.fragment);
    },
    m(l, i) {
      ut(e, l, i), t = !0;
    },
    p(l, i) {
      const o = {};
      i & /*download*/
      4 && (o.href = /*download*/
      l[2]), i & /*$$scope, i18n*/
      528 && (o.$$scope = { dirty: i, ctx: l }), e.$set(o);
    },
    i(l) {
      t || (K(e.$$.fragment, l), t = !0);
    },
    o(l) {
      fe(e.$$.fragment, l), t = !1;
    },
    d(l) {
      ft(e, l);
    }
  };
}
function Er(n) {
  let e, t;
  return e = new ze({
    props: {
      Icon: Nl,
      label: (
        /*i18n*/
        n[4]("common.download")
      )
    }
  }), {
    c() {
      rt(e.$$.fragment);
    },
    m(l, i) {
      ut(e, l, i), t = !0;
    },
    p(l, i) {
      const o = {};
      i & /*i18n*/
      16 && (o.label = /*i18n*/
      l[4]("common.download")), e.$set(o);
    },
    i(l) {
      t || (K(e.$$.fragment, l), t = !0);
    },
    o(l) {
      fe(e.$$.fragment, l), t = !1;
    },
    d(l) {
      ft(e, l);
    }
  };
}
function zr(n) {
  let e, t, l, i, o, r, f = (
    /*editable*/
    n[0] && al(n)
  ), a = (
    /*undoable*/
    n[1] && rl(n)
  ), s = (
    /*download*/
    n[2] && fl(n)
  );
  return o = new ze({
    props: {
      Icon: Bl,
      label: (
        /*i18n*/
        n[4]("common.clear")
      )
    }
  }), o.$on(
    "click",
    /*click_handler_2*/
    n[8]
  ), {
    c() {
      e = yr("div"), f && f.c(), t = xt(), a && a.c(), l = xt(), s && s.c(), i = xt(), rt(o.$$.fragment), pr(e, "class", "svelte-1wj0ocy"), sl(e, "not-absolute", !/*absolute*/
      n[3]), ol(
        e,
        "position",
        /*absolute*/
        n[3] ? "absolute" : "static"
      );
    },
    m(u, _) {
      qr(u, e, _), f && f.m(e, null), Kt(e, t), a && a.m(e, null), Kt(e, l), s && s.m(e, null), Kt(e, i), ut(o, e, null), r = !0;
    },
    p(u, [_]) {
      /*editable*/
      u[0] ? f ? (f.p(u, _), _ & /*editable*/
      1 && K(f, 1)) : (f = al(u), f.c(), K(f, 1), f.m(e, t)) : f && (Qt(), fe(f, 1, 1, () => {
        f = null;
      }), Jt()), /*undoable*/
      u[1] ? a ? (a.p(u, _), _ & /*undoable*/
      2 && K(a, 1)) : (a = rl(u), a.c(), K(a, 1), a.m(e, l)) : a && (Qt(), fe(a, 1, 1, () => {
        a = null;
      }), Jt()), /*download*/
      u[2] ? s ? (s.p(u, _), _ & /*download*/
      4 && K(s, 1)) : (s = fl(u), s.c(), K(s, 1), s.m(e, i)) : s && (Qt(), fe(s, 1, 1, () => {
        s = null;
      }), Jt());
      const c = {};
      _ & /*i18n*/
      16 && (c.label = /*i18n*/
      u[4]("common.clear")), o.$set(c), (!r || _ & /*absolute*/
      8) && sl(e, "not-absolute", !/*absolute*/
      u[3]), _ & /*absolute*/
      8 && ol(
        e,
        "position",
        /*absolute*/
        u[3] ? "absolute" : "static"
      );
    },
    i(u) {
      r || (K(f), K(a), K(s), K(o.$$.fragment, u), r = !0);
    },
    o(u) {
      fe(f), fe(a), fe(s), fe(o.$$.fragment, u), r = !1;
    },
    d(u) {
      u && vr(e), f && f.d(), a && a.d(), s && s.d(), ft(o);
    }
  };
}
function jr(n, e, t) {
  let { editable: l = !1 } = e, { undoable: i = !1 } = e, { download: o = null } = e, { absolute: r = !0 } = e, { i18n: f } = e;
  const a = Lr(), s = () => a("edit"), u = () => a("undo"), _ = (c) => {
    a("clear"), c.stopPropagation();
  };
  return n.$$set = (c) => {
    "editable" in c && t(0, l = c.editable), "undoable" in c && t(1, i = c.undoable), "download" in c && t(2, o = c.download), "absolute" in c && t(3, r = c.absolute), "i18n" in c && t(4, f = c.i18n);
  }, [
    l,
    i,
    o,
    r,
    f,
    a,
    s,
    u,
    _
  ];
}
class Ir extends kr {
  constructor(e) {
    super(), Cr(this, e, jr, zr, Sr, {
      editable: 0,
      undoable: 1,
      download: 2,
      absolute: 3,
      i18n: 4
    });
  }
}
function ui(n, e, t) {
  if (n == null)
    return null;
  if (Array.isArray(n)) {
    const l = [];
    for (const i of n)
      i == null ? l.push(null) : l.push(ui(i, e, t));
    return l;
  }
  return n.is_stream ? t == null ? new Yt({
    ...n,
    url: e + "/stream/" + n.path
  }) : new Yt({
    ...n,
    url: "/proxy=" + t + "stream/" + n.path
  }) : new Yt({
    ...n,
    url: Dr(n.path, e, t)
  });
}
function Mr(n) {
  try {
    const e = new URL(n);
    return e.protocol === "http:" || e.protocol === "https:";
  } catch {
    return !1;
  }
}
function Ar() {
  const n = document.querySelector(".gradio-container");
  if (!n)
    return "";
  const e = n.className.match(/gradio-container-(.+)/);
  return e ? e[1] : "";
}
const Rr = +Ar()[0];
function Dr(n, e, t) {
  const l = Rr >= 5 ? "gradio_api/" : "";
  return n == null ? t ? `/proxy=${t}${l}file=` : `${e}${l}file=` : Mr(n) ? n : t ? `/proxy=${t}${l}file=${n}` : `${e}/${l}file=${n}`;
}
var ul = Object.prototype.hasOwnProperty;
function _l(n, e, t) {
  for (t of n.keys())
    if (lt(t, e))
      return t;
}
function lt(n, e) {
  var t, l, i;
  if (n === e)
    return !0;
  if (n && e && (t = n.constructor) === e.constructor) {
    if (t === Date)
      return n.getTime() === e.getTime();
    if (t === RegExp)
      return n.toString() === e.toString();
    if (t === Array) {
      if ((l = n.length) === e.length)
        for (; l-- && lt(n[l], e[l]); )
          ;
      return l === -1;
    }
    if (t === Set) {
      if (n.size !== e.size)
        return !1;
      for (l of n)
        if (i = l, i && typeof i == "object" && (i = _l(e, i), !i) || !e.has(i))
          return !1;
      return !0;
    }
    if (t === Map) {
      if (n.size !== e.size)
        return !1;
      for (l of n)
        if (i = l[0], i && typeof i == "object" && (i = _l(e, i), !i) || !lt(l[1], e.get(i)))
          return !1;
      return !0;
    }
    if (t === ArrayBuffer)
      n = new Uint8Array(n), e = new Uint8Array(e);
    else if (t === DataView) {
      if ((l = n.byteLength) === e.byteLength)
        for (; l-- && n.getInt8(l) === e.getInt8(l); )
          ;
      return l === -1;
    }
    if (ArrayBuffer.isView(n)) {
      if ((l = n.byteLength) === e.byteLength)
        for (; l-- && n[l] === e[l]; )
          ;
      return l === -1;
    }
    if (!t || typeof n == "object") {
      l = 0;
      for (t in n)
        if (ul.call(n, t) && ++l && !ul.call(e, t) || !(t in e) || !lt(n[t], e[t]))
          return !1;
      return Object.keys(e).length === l;
    }
  }
  return n !== n && e !== e;
}
const {
  SvelteComponent: Fr,
  append: cl,
  attr: U,
  detach: Br,
  init: Nr,
  insert: Tr,
  noop: dl,
  safe_not_equal: Vr,
  svg_element: $t
} = window.__gradio__svelte__internal;
function Pr(n) {
  let e, t, l, i;
  return {
    c() {
      e = $t("svg"), t = $t("path"), l = $t("path"), U(t, "stroke", "currentColor"), U(t, "stroke-width", "1.5"), U(t, "stroke-linecap", "round"), U(t, "d", "M16.472 20H4.1a.6.6 0 0 1-.6-.6V9.6a.6.6 0 0 1 .6-.6h2.768a2 2 0 0 0 1.715-.971l2.71-4.517a1.631 1.631 0 0 1 2.961 1.308l-1.022 3.408a.6.6 0 0 0 .574.772h4.575a2 2 0 0 1 1.93 2.526l-1.91 7A2 2 0 0 1 16.473 20Z"), U(l, "stroke", "currentColor"), U(l, "stroke-width", "1.5"), U(l, "stroke-linecap", "round"), U(l, "stroke-linejoin", "round"), U(l, "d", "M7 20V9"), U(e, "xmlns", "http://www.w3.org/2000/svg"), U(e, "viewBox", "0 0 24 24"), U(e, "fill", i = /*selected*/
      n[0] ? "currentColor" : "none"), U(e, "stroke-width", "1.5"), U(e, "color", "currentColor"), U(e, "transform", "rotate(180)");
    },
    m(o, r) {
      Tr(o, e, r), cl(e, t), cl(e, l);
    },
    p(o, [r]) {
      r & /*selected*/
      1 && i !== (i = /*selected*/
      o[0] ? "currentColor" : "none") && U(e, "fill", i);
    },
    i: dl,
    o: dl,
    d(o) {
      o && Br(e);
    }
  };
}
function Or(n, e, t) {
  let { selected: l } = e;
  return n.$$set = (i) => {
    "selected" in i && t(0, l = i.selected);
  }, [l];
}
class Wr extends Fr {
  constructor(e) {
    super(), Nr(this, e, Or, Pr, Vr, { selected: 0 });
  }
}
const {
  SvelteComponent: Ur,
  append: Ee,
  attr: pe,
  check_outros: Zr,
  create_component: ml,
  destroy_component: hl,
  detach: At,
  element: We,
  flush: bt,
  group_outros: Hr,
  init: Gr,
  insert: Rt,
  listen: _i,
  mount_component: bl,
  safe_not_equal: Xr,
  set_data: ci,
  set_style: Yr,
  space: wt,
  src_url_equal: gl,
  text: di,
  transition_in: it,
  transition_out: St
} = window.__gradio__svelte__internal, { createEventDispatcher: Kr } = window.__gradio__svelte__internal;
function wl(n) {
  let e, t = (
    /*value*/
    n[0].caption + ""
  ), l;
  return {
    c() {
      e = We("div"), l = di(t), pe(e, "class", "foot-label left-label svelte-u350v8");
    },
    m(i, o) {
      Rt(i, e, o), Ee(e, l);
    },
    p(i, o) {
      o & /*value*/
      1 && t !== (t = /*value*/
      i[0].caption + "") && ci(l, t);
    },
    d(i) {
      i && At(e);
    }
  };
}
function kl(n) {
  let e, t, l, i;
  return {
    c() {
      e = We("button"), t = di(
        /*action_label*/
        n[3]
      ), pe(e, "class", "foot-label right-label svelte-u350v8");
    },
    m(o, r) {
      Rt(o, e, r), Ee(e, t), l || (i = _i(
        e,
        "click",
        /*click_handler_1*/
        n[6]
      ), l = !0);
    },
    p(o, r) {
      r & /*action_label*/
      8 && ci(
        t,
        /*action_label*/
        o[3]
      );
    },
    d(o) {
      o && At(e), l = !1, i();
    }
  };
}
function pl(n) {
  let e, t, l, i, o, r, f;
  return l = new ze({
    props: {
      size: "large",
      highlight: (
        /*value*/
        n[0].liked
      ),
      Icon: Fs
    }
  }), l.$on(
    "click",
    /*click_handler_2*/
    n[7]
  ), r = new ze({
    props: {
      size: "large",
      highlight: (
        /*value*/
        n[0].liked === !1
      ),
      Icon: Wr
    }
  }), r.$on(
    "click",
    /*click_handler_3*/
    n[8]
  ), {
    c() {
      e = We("div"), t = We("span"), ml(l.$$.fragment), i = wt(), o = We("span"), ml(r.$$.fragment), Yr(t, "margin-right", "1px"), pe(e, "class", "like-button svelte-u350v8");
    },
    m(a, s) {
      Rt(a, e, s), Ee(e, t), bl(l, t, null), Ee(e, i), Ee(e, o), bl(r, o, null), f = !0;
    },
    p(a, s) {
      const u = {};
      s & /*value*/
      1 && (u.highlight = /*value*/
      a[0].liked), l.$set(u);
      const _ = {};
      s & /*value*/
      1 && (_.highlight = /*value*/
      a[0].liked === !1), r.$set(_);
    },
    i(a) {
      f || (it(l.$$.fragment, a), it(r.$$.fragment, a), f = !0);
    },
    o(a) {
      St(l.$$.fragment, a), St(r.$$.fragment, a), f = !1;
    },
    d(a) {
      a && At(e), hl(l), hl(r);
    }
  };
}
function Jr(n) {
  let e, t, l, i, o, r, f, a, s, u, _ = (
    /*value*/
    n[0].caption && wl(n)
  ), c = (
    /*clickable*/
    n[2] && kl(n)
  ), d = (
    /*likeable*/
    n[1] && pl(n)
  );
  return {
    c() {
      e = We("div"), t = We("img"), o = wt(), _ && _.c(), r = wt(), c && c.c(), f = wt(), d && d.c(), pe(t, "alt", l = /*value*/
      n[0].caption || ""), gl(t.src, i = /*value*/
      n[0].image.url) || pe(t, "src", i), pe(t, "class", "thumbnail-img svelte-u350v8"), pe(t, "loading", "lazy"), pe(e, "class", "thumbnail-image-box svelte-u350v8");
    },
    m(h, y) {
      Rt(h, e, y), Ee(e, t), Ee(e, o), _ && _.m(e, null), Ee(e, r), c && c.m(e, null), Ee(e, f), d && d.m(e, null), a = !0, s || (u = _i(
        t,
        "click",
        /*click_handler*/
        n[5]
      ), s = !0);
    },
    p(h, [y]) {
      (!a || y & /*value*/
      1 && l !== (l = /*value*/
      h[0].caption || "")) && pe(t, "alt", l), (!a || y & /*value*/
      1 && !gl(t.src, i = /*value*/
      h[0].image.url)) && pe(t, "src", i), /*value*/
      h[0].caption ? _ ? _.p(h, y) : (_ = wl(h), _.c(), _.m(e, r)) : _ && (_.d(1), _ = null), /*clickable*/
      h[2] ? c ? c.p(h, y) : (c = kl(h), c.c(), c.m(e, f)) : c && (c.d(1), c = null), /*likeable*/
      h[1] ? d ? (d.p(h, y), y & /*likeable*/
      2 && it(d, 1)) : (d = pl(h), d.c(), it(d, 1), d.m(e, null)) : d && (Hr(), St(d, 1, 1, () => {
        d = null;
      }), Zr());
    },
    i(h) {
      a || (it(d), a = !0);
    },
    o(h) {
      St(d), a = !1;
    },
    d(h) {
      h && At(e), _ && _.d(), c && c.d(), d && d.d(), s = !1, u();
    }
  };
}
function Qr(n, e, t) {
  const l = Kr();
  let { likeable: i } = e, { clickable: o } = e, { value: r } = e, { action_label: f } = e;
  const a = () => l("click"), s = () => {
    l("label_click");
  }, u = () => {
    if (r.liked) {
      t(0, r.liked = void 0, r), l("like", void 0);
      return;
    }
    t(0, r.liked = !0, r), l("like", !0);
  }, _ = () => {
    if (r.liked === !1) {
      t(0, r.liked = void 0, r), l("like", void 0);
      return;
    }
    t(0, r.liked = !1, r), l("like", !1);
  };
  return n.$$set = (c) => {
    "likeable" in c && t(1, i = c.likeable), "clickable" in c && t(2, o = c.clickable), "value" in c && t(0, r = c.value), "action_label" in c && t(3, f = c.action_label);
  }, [
    r,
    i,
    o,
    f,
    l,
    a,
    s,
    u,
    _
  ];
}
class xr extends Ur {
  constructor(e) {
    super(), Gr(this, e, Qr, Jr, Xr, {
      likeable: 1,
      clickable: 2,
      value: 0,
      action_label: 3
    });
  }
  get likeable() {
    return this.$$.ctx[1];
  }
  set likeable(e) {
    this.$$set({ likeable: e }), bt();
  }
  get clickable() {
    return this.$$.ctx[2];
  }
  set clickable(e) {
    this.$$set({ clickable: e }), bt();
  }
  get value() {
    return this.$$.ctx[0];
  }
  set value(e) {
    this.$$set({ value: e }), bt();
  }
  get action_label() {
    return this.$$.ctx[3];
  }
  set action_label(e) {
    this.$$set({ action_label: e }), bt();
  }
}
const en = [
  {
    key: "xs",
    width: 0
  },
  {
    key: "sm",
    width: 576
  },
  {
    key: "md",
    width: 768
  },
  {
    key: "lg",
    width: 992
  },
  {
    key: "xl",
    width: 1200
  },
  {
    key: "xxl",
    width: 1600
  }
];
async function $r(n) {
  if ("clipboard" in navigator)
    await navigator.clipboard.writeText(n);
  else {
    const e = document.createElement("textarea");
    e.value = n, e.style.position = "absolute", e.style.left = "-999999px", document.body.prepend(e), e.select();
    try {
      document.execCommand("copy");
    } catch (t) {
      return Promise.reject(t);
    } finally {
      e.remove();
    }
  }
}
async function ef(n) {
  return n ? `<div style="display: flex; flex-wrap: wrap; gap: 16px">${(await Promise.all(
    n.map((t) => !t.image || !t.image.url ? "" : t.image.url)
  )).map((t) => `<img src="${t}" style="height: 400px" />`).join("")}</div>` : "";
}
function tf(n) {
  let e = 0;
  for (let t = 0; t < n.length; t++)
    e = n[e] <= n[t] ? e : t;
  return e;
}
function nf(n, {
  getWidth: e,
  setWidth: t,
  getHeight: l,
  setHeight: i,
  getPadding: o,
  setX: r,
  setY: f,
  getChildren: a
}, { cols: s, gap: u }) {
  const [_, c, d, h] = o(n), y = a(n), S = y.length, [v, k] = Array.isArray(u) ? u : [u, u];
  if (S) {
    const p = (e(n) - v * (s - 1) - (h + c)) / s;
    y.forEach((g) => {
      t(g, p);
    });
    const b = y.map((g) => l(g)), q = Array(s).fill(_);
    for (let g = 0; g < S; g++) {
      const L = y[g], C = tf(q);
      f(L, q[C]), r(L, h + (p + v) * C), q[C] += b[g] + k;
    }
    i(n, Math.max(...q) - k + d);
  } else
    i(n, _ + d);
}
const vl = (n) => n.nodeType == 1, fn = Symbol(), un = Symbol();
function lf(n, e) {
  let t, l, i = !1;
  function o() {
    i || (i = !0, requestAnimationFrame(() => {
      e(), n[un] = n.offsetWidth, n[fn] = n.offsetHeight, i = !1;
    }));
  }
  function r() {
    n && (t = new ResizeObserver((a) => {
      a.some((s) => {
        const u = s.target;
        return u[un] !== u.offsetWidth || u[fn] !== u.offsetHeight;
      }) && o();
    }), t.observe(n), Array.from(n.children).forEach((a) => {
      t.observe(a);
    }), l = new MutationObserver((a) => {
      a.forEach((s) => {
        s.addedNodes.forEach(
          (u) => vl(u) && t.observe(u)
        ), s.removedNodes.forEach(
          (u) => vl(u) && t.unobserve(u)
        );
      }), o();
    }), l.observe(n, { childList: !0, attributes: !1 }), o());
  }
  function f() {
    t == null || t.disconnect(), l == null || l.disconnect();
  }
  return { layout: o, mount: r, unmount: f };
}
const of = (n, e) => lf(n, () => {
  nf(
    n,
    {
      getWidth: (t) => t.offsetWidth,
      setWidth: (t, l) => t.style.width = l + "px",
      getHeight: (t) => (t[un] = t.offsetWidth, t[fn] = t.offsetHeight),
      setHeight: (t, l) => t.style.height = l + "px",
      getPadding: (t) => {
        const l = getComputedStyle(t);
        return [
          parseInt(l.paddingTop),
          parseInt(l.paddingRight),
          parseInt(l.paddingBottom),
          parseInt(l.paddingLeft)
        ];
      },
      setX: (t, l) => t.style.left = l + "px",
      setY: (t, l) => t.style.top = l + "px",
      getChildren: (t) => Array.from(t.children)
    },
    e
  );
});
class sf {
  constructor(e, t = {
    cols: 2,
    gap: 4
  }) {
    yn(this, "_layout");
    this._layout = of(e, t), this._layout.mount();
  }
  unmount() {
    this._layout.unmount();
  }
  render() {
    this._layout.layout();
  }
}
const {
  SvelteComponent: af,
  add_iframe_resize_listener: rf,
  add_render_callback: mi,
  append: W,
  assign: ff,
  attr: j,
  binding_callbacks: tn,
  bubble: uf,
  check_outros: Pe,
  create_component: je,
  destroy_component: Ie,
  destroy_each: hi,
  detach: ce,
  element: X,
  empty: _f,
  ensure_array_like: Lt,
  get_spread_object: cf,
  get_spread_update: df,
  globals: mf,
  group_outros: Oe,
  init: hf,
  insert: de,
  listen: Et,
  mount_component: Me,
  noop: bf,
  run_all: gf,
  safe_not_equal: wf,
  set_data: bi,
  set_style: Be,
  space: Ce,
  src_url_equal: zt,
  text: gi,
  toggle_class: te,
  transition_in: M,
  transition_out: D
} = window.__gradio__svelte__internal, { window: _n } = mf, { createEventDispatcher: kf, onDestroy: pf, tick: vf } = window.__gradio__svelte__internal;
function yl(n, e, t) {
  const l = n.slice();
  return l[57] = e[t], l[59] = t, l;
}
function Cl(n, e, t) {
  const l = n.slice();
  return l[57] = e[t], l[60] = e, l[59] = t, l;
}
function ql(n) {
  let e, t;
  return e = new ho({
    props: {
      show_label: (
        /*show_label*/
        n[2]
      ),
      Icon: Tl,
      label: (
        /*label*/
        n[4] || "Gallery"
      )
    }
  }), {
    c() {
      je(e.$$.fragment);
    },
    m(l, i) {
      Me(e, l, i), t = !0;
    },
    p(l, i) {
      const o = {};
      i[0] & /*show_label*/
      4 && (o.show_label = /*show_label*/
      l[2]), i[0] & /*label*/
      16 && (o.label = /*label*/
      l[4] || "Gallery"), e.$set(o);
    },
    i(l) {
      t || (M(e.$$.fragment, l), t = !0);
    },
    o(l) {
      D(e.$$.fragment, l), t = !1;
    },
    d(l) {
      Ie(e, l);
    }
  };
}
function yf(n) {
  let e, t, l, i, o, r, f, a, s, u, _, c = (
    /*selected_image*/
    n[23] && /*allow_preview*/
    n[9] && Sl(n)
  ), d = (
    /*show_share_button*/
    n[10] && jl(n)
  ), h = Lt(
    /*resolved_value*/
    n[18]
  ), y = [];
  for (let b = 0; b < h.length; b += 1)
    y[b] = Il(yl(n, h, b));
  const S = (b) => D(y[b], 1, 1, () => {
    y[b] = null;
  }), v = [Sf, qf], k = [];
  function p(b, q) {
    return (
      /*pending*/
      b[5] ? 0 : 1
    );
  }
  return a = p(n), s = k[a] = v[a](n), {
    c() {
      c && c.c(), e = Ce(), t = X("div"), l = X("div"), d && d.c(), i = Ce(), o = X("div");
      for (let b = 0; b < y.length; b += 1)
        y[b].c();
      r = Ce(), f = X("p"), s.c(), j(o, "class", "waterfall svelte-yk2d08"), j(l, "class", "grid-container svelte-yk2d08"), Be(
        l,
        "--object-fit",
        /*object_fit*/
        n[1]
      ), Be(
        l,
        "min-height",
        /*height*/
        n[8] + "px"
      ), te(
        l,
        "pt-6",
        /*show_label*/
        n[2]
      ), j(f, "class", "loading-line svelte-yk2d08"), te(f, "visible", !/*selected_image*/
      (n[23] && /*allow_preview*/
      n[9]) && /*has_more*/
      n[3]), j(t, "class", "grid-wrap svelte-yk2d08"), Be(
        t,
        "height",
        /*height*/
        n[8] + "px"
      ), mi(() => (
        /*div2_elementresize_handler*/
        n[51].call(t)
      )), te(t, "fixed-height", !/*height*/
      n[8] || /*height*/
      n[8] === "auto");
    },
    m(b, q) {
      c && c.m(b, q), de(b, e, q), de(b, t, q), W(t, l), d && d.m(l, null), W(l, i), W(l, o);
      for (let g = 0; g < y.length; g += 1)
        y[g] && y[g].m(o, null);
      n[49](o), W(t, r), W(t, f), k[a].m(f, null), u = rf(
        t,
        /*div2_elementresize_handler*/
        n[51].bind(t)
      ), _ = !0;
    },
    p(b, q) {
      if (/*selected_image*/
      b[23] && /*allow_preview*/
      b[9] ? c ? (c.p(b, q), q[0] & /*selected_image, allow_preview*/
      8389120 && M(c, 1)) : (c = Sl(b), c.c(), M(c, 1), c.m(e.parentNode, e)) : c && (Oe(), D(c, 1, 1, () => {
        c = null;
      }), Pe()), /*show_share_button*/
      b[10] ? d ? (d.p(b, q), q[0] & /*show_share_button*/
      1024 && M(d, 1)) : (d = jl(b), d.c(), M(d, 1), d.m(l, i)) : d && (Oe(), D(d, 1, 1, () => {
        d = null;
      }), Pe()), q[0] & /*resolved_value, selected_index, likeable, clickable, action_label, dispatch*/
      17045569) {
        h = Lt(
          /*resolved_value*/
          b[18]
        );
        let L;
        for (L = 0; L < h.length; L += 1) {
          const C = yl(b, h, L);
          y[L] ? (y[L].p(C, q), M(y[L], 1)) : (y[L] = Il(C), y[L].c(), M(y[L], 1), y[L].m(o, null));
        }
        for (Oe(), L = h.length; L < y.length; L += 1)
          S(L);
        Pe();
      }
      (!_ || q[0] & /*object_fit*/
      2) && Be(
        l,
        "--object-fit",
        /*object_fit*/
        b[1]
      ), (!_ || q[0] & /*height*/
      256) && Be(
        l,
        "min-height",
        /*height*/
        b[8] + "px"
      ), (!_ || q[0] & /*show_label*/
      4) && te(
        l,
        "pt-6",
        /*show_label*/
        b[2]
      );
      let g = a;
      a = p(b), a === g ? k[a].p(b, q) : (Oe(), D(k[g], 1, 1, () => {
        k[g] = null;
      }), Pe(), s = k[a], s ? s.p(b, q) : (s = k[a] = v[a](b), s.c()), M(s, 1), s.m(f, null)), (!_ || q[0] & /*selected_image, allow_preview, has_more*/
      8389128) && te(f, "visible", !/*selected_image*/
      (b[23] && /*allow_preview*/
      b[9]) && /*has_more*/
      b[3]), (!_ || q[0] & /*height*/
      256) && Be(
        t,
        "height",
        /*height*/
        b[8] + "px"
      ), (!_ || q[0] & /*height*/
      256) && te(t, "fixed-height", !/*height*/
      b[8] || /*height*/
      b[8] === "auto");
    },
    i(b) {
      if (!_) {
        M(c), M(d);
        for (let q = 0; q < h.length; q += 1)
          M(y[q]);
        M(s), _ = !0;
      }
    },
    o(b) {
      D(c), D(d), y = y.filter(Boolean);
      for (let q = 0; q < y.length; q += 1)
        D(y[q]);
      D(s), _ = !1;
    },
    d(b) {
      b && (ce(e), ce(t)), c && c.d(b), d && d.d(), hi(y, b), n[49](null), k[a].d(), u();
    }
  };
}
function Cf(n) {
  let e, t;
  return e = new Go({
    props: {
      unpadded_box: !0,
      size: "large",
      $$slots: { default: [Ef] },
      $$scope: { ctx: n }
    }
  }), {
    c() {
      je(e.$$.fragment);
    },
    m(l, i) {
      Me(e, l, i), t = !0;
    },
    p(l, i) {
      const o = {};
      i[1] & /*$$scope*/
      1073741824 && (o.$$scope = { dirty: i, ctx: l }), e.$set(o);
    },
    i(l) {
      t || (M(e.$$.fragment, l), t = !0);
    },
    o(l) {
      D(e.$$.fragment, l), t = !1;
    },
    d(l) {
      Ie(e, l);
    }
  };
}
function Sl(n) {
  var q;
  let e, t, l, i, o, r, f, a, s, u, _, c, d, h, y, S, v = (
    /*show_download_button*/
    n[13] && Ll(n)
  );
  i = new Ir({
    props: { i18n: (
      /*i18n*/
      n[14]
    ), absolute: !1 }
  }), i.$on(
    "clear",
    /*clear_handler*/
    n[39]
  );
  let k = (
    /*selected_image*/
    ((q = n[23]) == null ? void 0 : q.caption) && El(n)
  ), p = Lt(
    /*resolved_value*/
    n[18]
  ), b = [];
  for (let g = 0; g < p.length; g += 1)
    b[g] = zl(Cl(n, p, g));
  return {
    c() {
      e = X("button"), t = X("div"), v && v.c(), l = Ce(), je(i.$$.fragment), o = Ce(), r = X("button"), f = X("img"), _ = Ce(), k && k.c(), c = Ce(), d = X("div");
      for (let g = 0; g < b.length; g += 1)
        b[g].c();
      j(t, "class", "icon-buttons svelte-yk2d08"), j(f, "data-testid", "detailed-image"), zt(f.src, a = /*selected_image*/
      n[23].image.url) || j(f, "src", a), j(f, "alt", s = /*selected_image*/
      n[23].caption || ""), j(f, "title", u = /*selected_image*/
      n[23].caption || null), j(f, "loading", "lazy"), j(f, "class", "svelte-yk2d08"), te(f, "with-caption", !!/*selected_image*/
      n[23].caption), j(r, "class", "image-button svelte-yk2d08"), Be(r, "height", "calc(100% - " + /*selected_image*/
      (n[23].caption ? "80px" : "60px") + ")"), j(r, "aria-label", "detailed view of selected image"), j(d, "class", "thumbnails scroll-hide svelte-yk2d08"), j(d, "data-testid", "container_el"), j(e, "class", "preview svelte-yk2d08");
    },
    m(g, L) {
      de(g, e, L), W(e, t), v && v.m(t, null), W(t, l), Me(i, t, null), W(e, o), W(e, r), W(r, f), W(e, _), k && k.m(e, null), W(e, c), W(e, d);
      for (let C = 0; C < b.length; C += 1)
        b[C] && b[C].m(d, null);
      n[43](d), h = !0, y || (S = [
        Et(
          r,
          "click",
          /*click_handler_1*/
          n[40]
        ),
        Et(
          e,
          "keydown",
          /*on_keydown*/
          n[26]
        )
      ], y = !0);
    },
    p(g, L) {
      var P;
      /*show_download_button*/
      g[13] ? v ? (v.p(g, L), L[0] & /*show_download_button*/
      8192 && M(v, 1)) : (v = Ll(g), v.c(), M(v, 1), v.m(t, l)) : v && (Oe(), D(v, 1, 1, () => {
        v = null;
      }), Pe());
      const C = {};
      if (L[0] & /*i18n*/
      16384 && (C.i18n = /*i18n*/
      g[14]), i.$set(C), (!h || L[0] & /*selected_image*/
      8388608 && !zt(f.src, a = /*selected_image*/
      g[23].image.url)) && j(f, "src", a), (!h || L[0] & /*selected_image*/
      8388608 && s !== (s = /*selected_image*/
      g[23].caption || "")) && j(f, "alt", s), (!h || L[0] & /*selected_image*/
      8388608 && u !== (u = /*selected_image*/
      g[23].caption || null)) && j(f, "title", u), (!h || L[0] & /*selected_image*/
      8388608) && te(f, "with-caption", !!/*selected_image*/
      g[23].caption), (!h || L[0] & /*selected_image*/
      8388608) && Be(r, "height", "calc(100% - " + /*selected_image*/
      (g[23].caption ? "80px" : "60px") + ")"), /*selected_image*/
      (P = g[23]) != null && P.caption ? k ? k.p(g, L) : (k = El(g), k.c(), k.m(e, c)) : k && (k.d(1), k = null), L[0] & /*resolved_value, el, selected_index*/
      2359297) {
        p = Lt(
          /*resolved_value*/
          g[18]
        );
        let A;
        for (A = 0; A < p.length; A += 1) {
          const O = Cl(g, p, A);
          b[A] ? b[A].p(O, L) : (b[A] = zl(O), b[A].c(), b[A].m(d, null));
        }
        for (; A < b.length; A += 1)
          b[A].d(1);
        b.length = p.length;
      }
    },
    i(g) {
      h || (M(v), M(i.$$.fragment, g), h = !0);
    },
    o(g) {
      D(v), D(i.$$.fragment, g), h = !1;
    },
    d(g) {
      g && ce(e), v && v.d(), Ie(i), k && k.d(), hi(b, g), n[43](null), y = !1, gf(S);
    }
  };
}
function Ll(n) {
  let e, t, l;
  return t = new ze({
    props: {
      show_label: !0,
      label: (
        /*i18n*/
        n[14]("common.download")
      ),
      Icon: Nl
    }
  }), t.$on(
    "click",
    /*click_handler*/
    n[38]
  ), {
    c() {
      e = X("div"), je(t.$$.fragment), j(e, "class", "download-button-container svelte-yk2d08");
    },
    m(i, o) {
      de(i, e, o), Me(t, e, null), l = !0;
    },
    p(i, o) {
      const r = {};
      o[0] & /*i18n*/
      16384 && (r.label = /*i18n*/
      i[14]("common.download")), t.$set(r);
    },
    i(i) {
      l || (M(t.$$.fragment, i), l = !0);
    },
    o(i) {
      D(t.$$.fragment, i), l = !1;
    },
    d(i) {
      i && ce(e), Ie(t);
    }
  };
}
function El(n) {
  let e, t = (
    /*selected_image*/
    n[23].caption + ""
  ), l;
  return {
    c() {
      e = X("caption"), l = gi(t), j(e, "class", "caption svelte-yk2d08");
    },
    m(i, o) {
      de(i, e, o), W(e, l);
    },
    p(i, o) {
      o[0] & /*selected_image*/
      8388608 && t !== (t = /*selected_image*/
      i[23].caption + "") && bi(l, t);
    },
    d(i) {
      i && ce(e);
    }
  };
}
function zl(n) {
  let e, t, l, i, o, r, f = (
    /*i*/
    n[59]
  ), a, s;
  const u = () => (
    /*button_binding*/
    n[41](e, f)
  ), _ = () => (
    /*button_binding*/
    n[41](null, f)
  );
  function c() {
    return (
      /*click_handler_2*/
      n[42](
        /*i*/
        n[59]
      )
    );
  }
  return {
    c() {
      e = X("button"), t = X("img"), o = Ce(), zt(t.src, l = /*entry*/
      n[57].image.url) || j(t, "src", l), j(t, "title", i = /*entry*/
      n[57].caption || null), j(t, "data-testid", "thumbnail " + /*i*/
      (n[59] + 1)), j(t, "alt", ""), j(t, "loading", "lazy"), j(t, "class", "svelte-yk2d08"), j(e, "class", "thumbnail-item thumbnail-small svelte-yk2d08"), j(e, "aria-label", r = "Thumbnail " + /*i*/
      (n[59] + 1) + " of " + /*resolved_value*/
      n[18].length), te(
        e,
        "selected",
        /*selected_index*/
        n[0] === /*i*/
        n[59]
      );
    },
    m(d, h) {
      de(d, e, h), W(e, t), W(e, o), u(), a || (s = Et(e, "click", c), a = !0);
    },
    p(d, h) {
      n = d, h[0] & /*resolved_value*/
      262144 && !zt(t.src, l = /*entry*/
      n[57].image.url) && j(t, "src", l), h[0] & /*resolved_value*/
      262144 && i !== (i = /*entry*/
      n[57].caption || null) && j(t, "title", i), h[0] & /*resolved_value*/
      262144 && r !== (r = "Thumbnail " + /*i*/
      (n[59] + 1) + " of " + /*resolved_value*/
      n[18].length) && j(e, "aria-label", r), f !== /*i*/
      n[59] && (_(), f = /*i*/
      n[59], u()), h[0] & /*selected_index*/
      1 && te(
        e,
        "selected",
        /*selected_index*/
        n[0] === /*i*/
        n[59]
      );
    },
    d(d) {
      d && ce(e), _(), a = !1, s();
    }
  };
}
function jl(n) {
  let e, t, l;
  return t = new na({
    props: {
      i18n: (
        /*i18n*/
        n[14]
      ),
      value: (
        /*resolved_value*/
        n[18]
      ),
      formatter: ef
    }
  }), t.$on(
    "share",
    /*share_handler*/
    n[44]
  ), t.$on(
    "error",
    /*error_handler*/
    n[45]
  ), {
    c() {
      e = X("div"), je(t.$$.fragment), j(e, "class", "icon-button svelte-yk2d08");
    },
    m(i, o) {
      de(i, e, o), Me(t, e, null), l = !0;
    },
    p(i, o) {
      const r = {};
      o[0] & /*i18n*/
      16384 && (r.i18n = /*i18n*/
      i[14]), o[0] & /*resolved_value*/
      262144 && (r.value = /*resolved_value*/
      i[18]), t.$set(r);
    },
    i(i) {
      l || (M(t.$$.fragment, i), l = !0);
    },
    o(i) {
      D(t.$$.fragment, i), l = !1;
    },
    d(i) {
      i && ce(e), Ie(t);
    }
  };
}
function Il(n) {
  let e, t, l, i, o;
  function r() {
    return (
      /*click_handler_3*/
      n[46](
        /*i*/
        n[59]
      )
    );
  }
  function f() {
    return (
      /*label_click_handler*/
      n[47](
        /*i*/
        n[59],
        /*entry*/
        n[57]
      )
    );
  }
  function a(...s) {
    return (
      /*like_handler*/
      n[48](
        /*i*/
        n[59],
        /*entry*/
        n[57],
        ...s
      )
    );
  }
  return t = new xr({
    props: {
      likeable: (
        /*likeable*/
        n[11]
      ),
      clickable: (
        /*clickable*/
        n[12]
      ),
      value: (
        /*entry*/
        n[57]
      ),
      action_label: (
        /*action_label*/
        n[6]
      )
    }
  }), t.$on("click", r), t.$on("label_click", f), t.$on("like", a), {
    c() {
      e = X("div"), je(t.$$.fragment), l = Ce(), j(e, "class", "thumbnail-item thumbnail-lg svelte-yk2d08"), j(e, "aria-label", i = "Thumbnail " + /*i*/
      (n[59] + 1) + " of " + /*resolved_value*/
      n[18].length), te(
        e,
        "selected",
        /*selected_index*/
        n[0] === /*i*/
        n[59]
      );
    },
    m(s, u) {
      de(s, e, u), Me(t, e, null), W(e, l), o = !0;
    },
    p(s, u) {
      n = s;
      const _ = {};
      u[0] & /*likeable*/
      2048 && (_.likeable = /*likeable*/
      n[11]), u[0] & /*clickable*/
      4096 && (_.clickable = /*clickable*/
      n[12]), u[0] & /*resolved_value*/
      262144 && (_.value = /*entry*/
      n[57]), u[0] & /*action_label*/
      64 && (_.action_label = /*action_label*/
      n[6]), t.$set(_), (!o || u[0] & /*resolved_value*/
      262144 && i !== (i = "Thumbnail " + /*i*/
      (n[59] + 1) + " of " + /*resolved_value*/
      n[18].length)) && j(e, "aria-label", i), (!o || u[0] & /*selected_index*/
      1) && te(
        e,
        "selected",
        /*selected_index*/
        n[0] === /*i*/
        n[59]
      );
    },
    i(s) {
      o || (M(t.$$.fragment, s), o = !0);
    },
    o(s) {
      D(t.$$.fragment, s), o = !1;
    },
    d(s) {
      s && ce(e), Ie(t);
    }
  };
}
function qf(n) {
  let e, t;
  const l = [
    /*load_more_button_props*/
    n[15]
  ];
  let i = {
    $$slots: { default: [Lf] },
    $$scope: { ctx: n }
  };
  for (let o = 0; o < l.length; o += 1)
    i = ff(i, l[o]);
  return e = new Ka({ props: i }), e.$on(
    "click",
    /*click_handler_4*/
    n[50]
  ), {
    c() {
      je(e.$$.fragment);
    },
    m(o, r) {
      Me(e, o, r), t = !0;
    },
    p(o, r) {
      const f = r[0] & /*load_more_button_props*/
      32768 ? df(l, [cf(
        /*load_more_button_props*/
        o[15]
      )]) : {};
      r[0] & /*i18n, load_more_button_props*/
      49152 | r[1] & /*$$scope*/
      1073741824 && (f.$$scope = { dirty: r, ctx: o }), e.$set(f);
    },
    i(o) {
      t || (M(e.$$.fragment, o), t = !0);
    },
    o(o) {
      D(e.$$.fragment, o), t = !1;
    },
    d(o) {
      Ie(e, o);
    }
  };
}
function Sf(n) {
  let e, t;
  return e = new Wl({ props: { margin: !1 } }), {
    c() {
      je(e.$$.fragment);
    },
    m(l, i) {
      Me(e, l, i), t = !0;
    },
    p: bf,
    i(l) {
      t || (M(e.$$.fragment, l), t = !0);
    },
    o(l) {
      D(e.$$.fragment, l), t = !1;
    },
    d(l) {
      Ie(e, l);
    }
  };
}
function Lf(n) {
  let e = (
    /*i18n*/
    n[14](
      /*load_more_button_props*/
      n[15].value || /*load_more_button_props*/
      n[15].label || "Load More"
    ) + ""
  ), t;
  return {
    c() {
      t = gi(e);
    },
    m(l, i) {
      de(l, t, i);
    },
    p(l, i) {
      i[0] & /*i18n, load_more_button_props*/
      49152 && e !== (e = /*i18n*/
      l[14](
        /*load_more_button_props*/
        l[15].value || /*load_more_button_props*/
        l[15].label || "Load More"
      ) + "") && bi(t, e);
    },
    d(l) {
      l && ce(t);
    }
  };
}
function Ef(n) {
  let e, t;
  return e = new Tl({}), {
    c() {
      je(e.$$.fragment);
    },
    m(l, i) {
      Me(e, l, i), t = !0;
    },
    i(l) {
      t || (M(e.$$.fragment, l), t = !0);
    },
    o(l) {
      D(e.$$.fragment, l), t = !1;
    },
    d(l) {
      Ie(e, l);
    }
  };
}
function zf(n) {
  let e, t, l, i, o, r, f;
  mi(
    /*onwindowresize*/
    n[37]
  );
  let a = (
    /*show_label*/
    n[2] && ql(n)
  );
  const s = [Cf, yf], u = [];
  function _(c, d) {
    return !/*value*/
    c[7] || !/*resolved_value*/
    c[18] || /*resolved_value*/
    c[18].length === 0 ? 0 : 1;
  }
  return t = _(n), l = u[t] = s[t](n), {
    c() {
      a && a.c(), e = Ce(), l.c(), i = _f();
    },
    m(c, d) {
      a && a.m(c, d), de(c, e, d), u[t].m(c, d), de(c, i, d), o = !0, r || (f = Et(
        _n,
        "resize",
        /*onwindowresize*/
        n[37]
      ), r = !0);
    },
    p(c, d) {
      /*show_label*/
      c[2] ? a ? (a.p(c, d), d[0] & /*show_label*/
      4 && M(a, 1)) : (a = ql(c), a.c(), M(a, 1), a.m(e.parentNode, e)) : a && (Oe(), D(a, 1, 1, () => {
        a = null;
      }), Pe());
      let h = t;
      t = _(c), t === h ? u[t].p(c, d) : (Oe(), D(u[h], 1, 1, () => {
        u[h] = null;
      }), Pe(), l = u[t], l ? l.p(c, d) : (l = u[t] = s[t](c), l.c()), M(l, 1), l.m(i.parentNode, i));
    },
    i(c) {
      o || (M(a), M(l), o = !0);
    },
    o(c) {
      D(a), D(l), o = !1;
    },
    d(c) {
      c && (ce(e), ce(i)), a && a.d(c), u[t].d(c), r = !1, f();
    }
  };
}
async function jf(n, e) {
  let t;
  try {
    t = await fetch(n);
  } catch (r) {
    if (r instanceof TypeError) {
      window.open(n, "_blank", "noreferrer");
      return;
    }
    throw r;
  }
  const l = await t.blob(), i = URL.createObjectURL(l), o = document.createElement("a");
  o.href = i, o.download = e, o.click(), URL.revokeObjectURL(i);
}
function If(n, e, t) {
  let l, i, o, { object_fit: r = "cover" } = e, { show_label: f = !0 } = e, { has_more: a = !1 } = e, { label: s } = e, { pending: u } = e, { action_label: _ } = e, { value: c = null } = e, { columns: d = [2] } = e, { height: h = "auto" } = e, { preview: y } = e, { root: S } = e, { proxy_url: v } = e, { allow_preview: k = !0 } = e, { show_share_button: p = !1 } = e, { likeable: b } = e, { clickable: q } = e, { show_download_button: g = !1 } = e, { i18n: L } = e, { selected_index: C = null } = e, { gap: P = 8 } = e, { load_more_button_props: A = {} } = e, O, B = [], me, Z = 0, he = 0, H = 0;
  const ie = kf();
  let qe = !0, Q = null, N = null, be = c;
  C == null && y && (c != null && c.length) && (C = 0);
  let Te = C;
  function He(w) {
    const V = w.target, ge = w.clientX, Dt = V.offsetWidth / 2;
    ge < Dt ? t(0, C = l) : t(0, C = i);
  }
  function et(w) {
    switch (w.code) {
      case "Escape":
        w.preventDefault(), t(0, C = null);
        break;
      case "ArrowLeft":
        w.preventDefault(), t(0, C = l);
        break;
      case "ArrowRight":
        w.preventDefault(), t(0, C = i);
        break;
    }
  }
  const m = [];
  let Ae;
  async function wi(w) {
    var vn;
    if (typeof w != "number" || (await vf(), m[w] === void 0))
      return;
    (vn = m[w]) == null || vn.focus();
    const { left: V, width: ge } = Ae.getBoundingClientRect(), { left: kn, width: Dt } = m[w].getBoundingClientRect(), pn = kn - V + Dt / 2 - ge / 2 + Ae.scrollLeft;
    Ae && typeof Ae.scrollTo == "function" && Ae.scrollTo({
      left: pn < 0 ? 0 : pn,
      behavior: "smooth"
    });
  }
  function ki() {
    Q == null || Q.unmount(), Q = new sf(O, { cols: me, gap: P });
  }
  pf(() => {
    Q == null || Q.unmount();
  });
  function pi() {
    t(20, he = _n.innerHeight), t(17, H = _n.innerWidth);
  }
  const vi = () => {
    const w = o == null ? void 0 : o.image;
    if (!w)
      return;
    const { url: V, orig_name: ge } = w;
    V && jf(V, ge ?? "image");
  }, yi = () => t(0, C = null), Ci = (w) => He(w);
  function qi(w, V) {
    tn[w ? "unshift" : "push"](() => {
      m[V] = w, t(21, m);
    });
  }
  const Si = (w) => t(0, C = w);
  function Li(w) {
    tn[w ? "unshift" : "push"](() => {
      Ae = w, t(22, Ae);
    });
  }
  const Ei = (w) => {
    $r(w.detail.description);
  };
  function zi(w) {
    uf.call(this, n, w);
  }
  const ji = (w) => t(0, C = w), Ii = (w, V) => {
    ie("click", { index: w, value: V });
  }, Mi = (w, V, ge) => {
    ie("like", { index: w, value: V, liked: ge.detail });
  };
  function Ai(w) {
    tn[w ? "unshift" : "push"](() => {
      O = w, t(16, O);
    });
  }
  const Ri = () => {
    ie("load_more");
  };
  function Di() {
    Z = this.clientHeight, t(19, Z);
  }
  return n.$$set = (w) => {
    "object_fit" in w && t(1, r = w.object_fit), "show_label" in w && t(2, f = w.show_label), "has_more" in w && t(3, a = w.has_more), "label" in w && t(4, s = w.label), "pending" in w && t(5, u = w.pending), "action_label" in w && t(6, _ = w.action_label), "value" in w && t(7, c = w.value), "columns" in w && t(27, d = w.columns), "height" in w && t(8, h = w.height), "preview" in w && t(28, y = w.preview), "root" in w && t(29, S = w.root), "proxy_url" in w && t(30, v = w.proxy_url), "allow_preview" in w && t(9, k = w.allow_preview), "show_share_button" in w && t(10, p = w.show_share_button), "likeable" in w && t(11, b = w.likeable), "clickable" in w && t(12, q = w.clickable), "show_download_button" in w && t(13, g = w.show_download_button), "i18n" in w && t(14, L = w.i18n), "selected_index" in w && t(0, C = w.selected_index), "gap" in w && t(31, P = w.gap), "load_more_button_props" in w && t(15, A = w.load_more_button_props);
  }, n.$$.update = () => {
    if (n.$$.dirty[0] & /*columns*/
    134217728)
      if (typeof d == "object" && d !== null)
        if (Array.isArray(d)) {
          const w = d.length;
          t(32, B = en.map((V, ge) => [V.width, d[ge] ?? d[w - 1]]));
        } else {
          let w = 0;
          t(32, B = en.map((V) => (w = d[V.key] ?? w, [V.width, w])));
        }
      else
        t(32, B = en.map((w) => [w.width, d]));
    if (n.$$.dirty[0] & /*window_width*/
    131072 | n.$$.dirty[1] & /*breakpointColumns*/
    2) {
      for (const [w, V] of [...B].reverse())
        if (H >= w) {
          t(33, me = V);
          break;
        }
    }
    n.$$.dirty[0] & /*value*/
    128 | n.$$.dirty[1] & /*was_reset*/
    8 && t(34, qe = c == null || c.length === 0 ? !0 : qe), n.$$.dirty[0] & /*value, root, proxy_url*/
    1610612864 && t(18, N = c == null ? null : c.map((w) => (w.image = ui(w.image, S, v), w))), n.$$.dirty[0] & /*value, preview, selected_index*/
    268435585 | n.$$.dirty[1] & /*prev_value, was_reset*/
    24 && (lt(be, c) || (qe ? (t(0, C = y && (c != null && c.length) ? 0 : null), t(34, qe = !1), Q = null) : t(
      0,
      C = C != null && c != null && C < c.length ? C : null
    ), ie("change"), t(35, be = c))), n.$$.dirty[0] & /*selected_index, resolved_value*/
    262145 && (l = ((C ?? 0) + ((N == null ? void 0 : N.length) ?? 0) - 1) % ((N == null ? void 0 : N.length) ?? 0)), n.$$.dirty[0] & /*selected_index, resolved_value*/
    262145 && (i = ((C ?? 0) + 1) % ((N == null ? void 0 : N.length) ?? 0)), n.$$.dirty[0] & /*selected_index, resolved_value*/
    262145 | n.$$.dirty[1] & /*old_selected_index*/
    32 && C !== Te && (t(36, Te = C), C !== null && ie("select", {
      index: C,
      value: N == null ? void 0 : N[C]
    })), n.$$.dirty[0] & /*allow_preview, selected_index*/
    513 && k && wi(C), n.$$.dirty[0] & /*waterfall_grid_el*/
    65536 | n.$$.dirty[1] & /*cols*/
    4 && O && ki(), n.$$.dirty[0] & /*selected_index, resolved_value*/
    262145 && t(23, o = C != null && N != null ? N[C] : null);
  }, [
    C,
    r,
    f,
    a,
    s,
    u,
    _,
    c,
    h,
    k,
    p,
    b,
    q,
    g,
    L,
    A,
    O,
    H,
    N,
    Z,
    he,
    m,
    Ae,
    o,
    ie,
    He,
    et,
    d,
    y,
    S,
    v,
    P,
    B,
    me,
    qe,
    be,
    Te,
    pi,
    vi,
    yi,
    Ci,
    qi,
    Si,
    Li,
    Ei,
    zi,
    ji,
    Ii,
    Mi,
    Ai,
    Ri,
    Di
  ];
}
class Mf extends af {
  constructor(e) {
    super(), hf(
      this,
      e,
      If,
      zf,
      wf,
      {
        object_fit: 1,
        show_label: 2,
        has_more: 3,
        label: 4,
        pending: 5,
        action_label: 6,
        value: 7,
        columns: 27,
        height: 8,
        preview: 28,
        root: 29,
        proxy_url: 30,
        allow_preview: 9,
        show_share_button: 10,
        likeable: 11,
        clickable: 12,
        show_download_button: 13,
        i18n: 14,
        selected_index: 0,
        gap: 31,
        load_more_button_props: 15
      },
      null,
      [-1, -1]
    );
  }
}
const {
  SvelteComponent: Af,
  add_flush_callback: Rf,
  assign: Df,
  bind: Ff,
  binding_callbacks: Bf,
  check_outros: Nf,
  create_component: bn,
  destroy_component: gn,
  detach: Tf,
  get_spread_object: Vf,
  get_spread_update: Pf,
  group_outros: Of,
  init: Wf,
  insert: Uf,
  mount_component: wn,
  safe_not_equal: Zf,
  space: Hf,
  transition_in: Qe,
  transition_out: ot
} = window.__gradio__svelte__internal, { createEventDispatcher: Gf } = window.__gradio__svelte__internal;
function Ml(n) {
  let e, t;
  const l = [
    {
      autoscroll: (
        /*gradio*/
        n[25].autoscroll
      )
    },
    { i18n: (
      /*gradio*/
      n[25].i18n
    ) },
    /*loading_status*/
    n[1],
    {
      show_progress: (
        /*loading_status*/
        n[1].show_progress === "hidden" ? "hidden" : (
          /*has_more*/
          n[3] ? "minimal" : (
            /*loading_status*/
            n[1].show_progress
          )
        )
      )
    }
  ];
  let i = {};
  for (let o = 0; o < l.length; o += 1)
    i = Df(i, l[o]);
  return e = new Ba({ props: i }), {
    c() {
      bn(e.$$.fragment);
    },
    m(o, r) {
      wn(e, o, r), t = !0;
    },
    p(o, r) {
      const f = r[0] & /*gradio, loading_status, has_more*/
      33554442 ? Pf(l, [
        r[0] & /*gradio*/
        33554432 && {
          autoscroll: (
            /*gradio*/
            o[25].autoscroll
          )
        },
        r[0] & /*gradio*/
        33554432 && { i18n: (
          /*gradio*/
          o[25].i18n
        ) },
        r[0] & /*loading_status*/
        2 && Vf(
          /*loading_status*/
          o[1]
        ),
        r[0] & /*loading_status, has_more*/
        10 && {
          show_progress: (
            /*loading_status*/
            o[1].show_progress === "hidden" ? "hidden" : (
              /*has_more*/
              o[3] ? "minimal" : (
                /*loading_status*/
                o[1].show_progress
              )
            )
          )
        }
      ]) : {};
      e.$set(f);
    },
    i(o) {
      t || (Qe(e.$$.fragment, o), t = !0);
    },
    o(o) {
      ot(e.$$.fragment, o), t = !1;
    },
    d(o) {
      gn(e, o);
    }
  };
}
function Xf(n) {
  var a;
  let e, t, l, i, o = (
    /*loading_status*/
    n[1] && Ml(n)
  );
  function r(s) {
    n[29](s);
  }
  let f = {
    pending: (
      /*loading_status*/
      ((a = n[1]) == null ? void 0 : a.status) === "pending"
    ),
    likeable: (
      /*likeable*/
      n[10]
    ),
    clickable: (
      /*clickable*/
      n[11]
    ),
    label: (
      /*label*/
      n[4]
    ),
    action_label: (
      /*action_label*/
      n[5]
    ),
    value: (
      /*value*/
      n[9]
    ),
    root: (
      /*root*/
      n[23]
    ),
    proxy_url: (
      /*proxy_url*/
      n[24]
    ),
    show_label: (
      /*show_label*/
      n[2]
    ),
    object_fit: (
      /*object_fit*/
      n[21]
    ),
    load_more_button_props: (
      /*_load_more_button_props*/
      n[26]
    ),
    has_more: (
      /*has_more*/
      n[3]
    ),
    columns: (
      /*columns*/
      n[15]
    ),
    height: (
      /*height*/
      n[17]
    ),
    preview: (
      /*preview*/
      n[18]
    ),
    gap: (
      /*gap*/
      n[16]
    ),
    allow_preview: (
      /*allow_preview*/
      n[19]
    ),
    show_share_button: (
      /*show_share_button*/
      n[20]
    ),
    show_download_button: (
      /*show_download_button*/
      n[22]
    ),
    i18n: (
      /*gradio*/
      n[25].i18n
    )
  };
  return (
    /*selected_index*/
    n[0] !== void 0 && (f.selected_index = /*selected_index*/
    n[0]), t = new Mf({ props: f }), Bf.push(() => Ff(t, "selected_index", r)), t.$on(
      "click",
      /*click_handler*/
      n[30]
    ), t.$on(
      "change",
      /*change_handler*/
      n[31]
    ), t.$on(
      "like",
      /*like_handler*/
      n[32]
    ), t.$on(
      "select",
      /*select_handler*/
      n[33]
    ), t.$on(
      "share",
      /*share_handler*/
      n[34]
    ), t.$on(
      "error",
      /*error_handler*/
      n[35]
    ), t.$on(
      "load_more",
      /*load_more_handler*/
      n[36]
    ), {
      c() {
        o && o.c(), e = Hf(), bn(t.$$.fragment);
      },
      m(s, u) {
        o && o.m(s, u), Uf(s, e, u), wn(t, s, u), i = !0;
      },
      p(s, u) {
        var c;
        /*loading_status*/
        s[1] ? o ? (o.p(s, u), u[0] & /*loading_status*/
        2 && Qe(o, 1)) : (o = Ml(s), o.c(), Qe(o, 1), o.m(e.parentNode, e)) : o && (Of(), ot(o, 1, 1, () => {
          o = null;
        }), Nf());
        const _ = {};
        u[0] & /*loading_status*/
        2 && (_.pending = /*loading_status*/
        ((c = s[1]) == null ? void 0 : c.status) === "pending"), u[0] & /*likeable*/
        1024 && (_.likeable = /*likeable*/
        s[10]), u[0] & /*clickable*/
        2048 && (_.clickable = /*clickable*/
        s[11]), u[0] & /*label*/
        16 && (_.label = /*label*/
        s[4]), u[0] & /*action_label*/
        32 && (_.action_label = /*action_label*/
        s[5]), u[0] & /*value*/
        512 && (_.value = /*value*/
        s[9]), u[0] & /*root*/
        8388608 && (_.root = /*root*/
        s[23]), u[0] & /*proxy_url*/
        16777216 && (_.proxy_url = /*proxy_url*/
        s[24]), u[0] & /*show_label*/
        4 && (_.show_label = /*show_label*/
        s[2]), u[0] & /*object_fit*/
        2097152 && (_.object_fit = /*object_fit*/
        s[21]), u[0] & /*_load_more_button_props*/
        67108864 && (_.load_more_button_props = /*_load_more_button_props*/
        s[26]), u[0] & /*has_more*/
        8 && (_.has_more = /*has_more*/
        s[3]), u[0] & /*columns*/
        32768 && (_.columns = /*columns*/
        s[15]), u[0] & /*height*/
        131072 && (_.height = /*height*/
        s[17]), u[0] & /*preview*/
        262144 && (_.preview = /*preview*/
        s[18]), u[0] & /*gap*/
        65536 && (_.gap = /*gap*/
        s[16]), u[0] & /*allow_preview*/
        524288 && (_.allow_preview = /*allow_preview*/
        s[19]), u[0] & /*show_share_button*/
        1048576 && (_.show_share_button = /*show_share_button*/
        s[20]), u[0] & /*show_download_button*/
        4194304 && (_.show_download_button = /*show_download_button*/
        s[22]), u[0] & /*gradio*/
        33554432 && (_.i18n = /*gradio*/
        s[25].i18n), !l && u[0] & /*selected_index*/
        1 && (l = !0, _.selected_index = /*selected_index*/
        s[0], Rf(() => l = !1)), t.$set(_);
      },
      i(s) {
        i || (Qe(o), Qe(t.$$.fragment, s), i = !0);
      },
      o(s) {
        ot(o), ot(t.$$.fragment, s), i = !1;
      },
      d(s) {
        s && Tf(e), o && o.d(s), gn(t, s);
      }
    }
  );
}
function Yf(n) {
  let e, t;
  return e = new xi({
    props: {
      visible: (
        /*visible*/
        n[8]
      ),
      variant: "solid",
      padding: !1,
      elem_id: (
        /*elem_id*/
        n[6]
      ),
      elem_classes: (
        /*elem_classes*/
        n[7]
      ),
      container: (
        /*container*/
        n[12]
      ),
      scale: (
        /*scale*/
        n[13]
      ),
      min_width: (
        /*min_width*/
        n[14]
      ),
      allow_overflow: !1,
      $$slots: { default: [Xf] },
      $$scope: { ctx: n }
    }
  }), {
    c() {
      bn(e.$$.fragment);
    },
    m(l, i) {
      wn(e, l, i), t = !0;
    },
    p(l, i) {
      const o = {};
      i[0] & /*visible*/
      256 && (o.visible = /*visible*/
      l[8]), i[0] & /*elem_id*/
      64 && (o.elem_id = /*elem_id*/
      l[6]), i[0] & /*elem_classes*/
      128 && (o.elem_classes = /*elem_classes*/
      l[7]), i[0] & /*container*/
      4096 && (o.container = /*container*/
      l[12]), i[0] & /*scale*/
      8192 && (o.scale = /*scale*/
      l[13]), i[0] & /*min_width*/
      16384 && (o.min_width = /*min_width*/
      l[14]), i[0] & /*loading_status, likeable, clickable, label, action_label, value, root, proxy_url, show_label, object_fit, _load_more_button_props, has_more, columns, height, preview, gap, allow_preview, show_share_button, show_download_button, gradio, selected_index*/
      134188607 | i[1] & /*$$scope*/
      128 && (o.$$scope = { dirty: i, ctx: l }), e.$set(o);
    },
    i(l) {
      t || (Qe(e.$$.fragment, l), t = !0);
    },
    o(l) {
      ot(e.$$.fragment, l), t = !1;
    },
    d(l) {
      gn(e, l);
    }
  };
}
function Kf(n, e, t) {
  let { loading_status: l } = e, { show_label: i } = e, { has_more: o } = e, { label: r } = e, { action_label: f } = e, { elem_id: a = "" } = e, { elem_classes: s = [] } = e, { visible: u = !0 } = e, { value: _ = null } = e, { likeable: c } = e, { clickable: d } = e, { container: h = !0 } = e, { scale: y = null } = e, { min_width: S = void 0 } = e, { columns: v = [2] } = e, { gap: k = 8 } = e, { height: p = "auto" } = e, { preview: b } = e, { allow_preview: q = !0 } = e, { selected_index: g = null } = e, { show_share_button: L = !1 } = e, { object_fit: C = "cover" } = e, { show_download_button: P = !1 } = e, { root: A } = e, { proxy_url: O } = e, { gradio: B } = e, { load_more_button_props: me = {} } = e, Z = {};
  const he = Gf(), H = (m) => {
    B.dispatch("like", m);
  };
  function ie(m) {
    g = m, t(0, g);
  }
  const qe = (m) => B.dispatch("click", m.detail), Q = () => B.dispatch("change", _), N = (m) => H(m.detail), be = (m) => B.dispatch("select", m.detail), Te = (m) => B.dispatch("share", m.detail), He = (m) => B.dispatch("error", m.detail), et = () => {
    B.dispatch("load_more", _);
  };
  return n.$$set = (m) => {
    "loading_status" in m && t(1, l = m.loading_status), "show_label" in m && t(2, i = m.show_label), "has_more" in m && t(3, o = m.has_more), "label" in m && t(4, r = m.label), "action_label" in m && t(5, f = m.action_label), "elem_id" in m && t(6, a = m.elem_id), "elem_classes" in m && t(7, s = m.elem_classes), "visible" in m && t(8, u = m.visible), "value" in m && t(9, _ = m.value), "likeable" in m && t(10, c = m.likeable), "clickable" in m && t(11, d = m.clickable), "container" in m && t(12, h = m.container), "scale" in m && t(13, y = m.scale), "min_width" in m && t(14, S = m.min_width), "columns" in m && t(15, v = m.columns), "gap" in m && t(16, k = m.gap), "height" in m && t(17, p = m.height), "preview" in m && t(18, b = m.preview), "allow_preview" in m && t(19, q = m.allow_preview), "selected_index" in m && t(0, g = m.selected_index), "show_share_button" in m && t(20, L = m.show_share_button), "object_fit" in m && t(21, C = m.object_fit), "show_download_button" in m && t(22, P = m.show_download_button), "root" in m && t(23, A = m.root), "proxy_url" in m && t(24, O = m.proxy_url), "gradio" in m && t(25, B = m.gradio), "load_more_button_props" in m && t(28, me = m.load_more_button_props);
  }, n.$$.update = () => {
    n.$$.dirty[0] & /*_load_more_button_props, load_more_button_props*/
    335544320 && t(26, Z = {
      ...Z,
      ...me
    }), n.$$.dirty[0] & /*selected_index*/
    1 && he("prop_change", { selected_index: g });
  }, [
    g,
    l,
    i,
    o,
    r,
    f,
    a,
    s,
    u,
    _,
    c,
    d,
    h,
    y,
    S,
    v,
    k,
    p,
    b,
    q,
    L,
    C,
    P,
    A,
    O,
    B,
    Z,
    H,
    me,
    ie,
    qe,
    Q,
    N,
    be,
    Te,
    He,
    et
  ];
}
class tu extends Af {
  constructor(e) {
    super(), Wf(
      this,
      e,
      Kf,
      Yf,
      Zf,
      {
        loading_status: 1,
        show_label: 2,
        has_more: 3,
        label: 4,
        action_label: 5,
        elem_id: 6,
        elem_classes: 7,
        visible: 8,
        value: 9,
        likeable: 10,
        clickable: 11,
        container: 12,
        scale: 13,
        min_width: 14,
        columns: 15,
        gap: 16,
        height: 17,
        preview: 18,
        allow_preview: 19,
        selected_index: 0,
        show_share_button: 20,
        object_fit: 21,
        show_download_button: 22,
        root: 23,
        proxy_url: 24,
        gradio: 25,
        load_more_button_props: 28
      },
      null,
      [-1, -1]
    );
  }
}
export {
  Mf as BaseGallery,
  tu as default
};
