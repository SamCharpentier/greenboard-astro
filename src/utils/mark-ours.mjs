import { defineHastPlugin } from "satteri";

/**
 * Marks the Greenboard column in a Markdown table, the way the comparison
 * pages highlight it. Runs when the site is built; the Sanity table
 * serializer does the same once the posts move there.
 */
const NAME = "Greenboard";

const text = (node) =>
  node.type === "text" ? node.value : (node.children ?? []).map(text).join("");

const elements = (node) => (node?.children ?? []).filter((child) => child.type === "element");

export default defineHastPlugin({
  name: "mark-ours",
  element: {
    filter: ["th", "td"],
    visit(cell, ctx) {
      const row = ctx.parent(cell);
      const group = row && ctx.parent(row);
      const table = group?.tagName === "table" ? group : group && ctx.parent(group);
      if (table?.tagName !== "table") return;
      const head = elements(table).find((child) => child.tagName === "thead");
      const headers = elements(elements(head)[0]);
      const column = headers.findIndex((header) => text(header).trim() === NAME);
      if (column < 1) return;
      const position = ctx.indexOf(cell) ?? -1;
      const index = row.children
        .slice(0, position)
        .filter((child) => child.type === "element").length;
      if (index !== column) return;
      const current = cell.properties?.className ?? [];
      ctx.setProperty(cell, "className", [...current, "is-ours"]);
    },
  },
});
