const OWNER_NAMES = new Set(["Zeng-Zhao Li", "Z.-Z. Li"]);

function el(tag, className, text) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text) node.textContent = text;
  return node;
}

function renderAuthors(authors) {
  const fragment = document.createDocumentFragment();
  authors.forEach((author, index) => {
    if (index) fragment.append(document.createTextNode(index === authors.length - 1 ? " and " : ", "));
    fragment.append(OWNER_NAMES.has(author) ? el("strong", "", author) : document.createTextNode(author));
  });
  return fragment;
}

function publicationEntry(pub) {
  const article = el("article", "publication");
  const heading = el("h3");
  const titleLink = el("a", "", pub.title);
  titleLink.href = pub.journal_url || pub.doi || pub.arxiv || pub.pdf || "#";
  heading.append(titleLink);
  const authors = el("p", "authors");
  authors.append(renderAuthors(pub.authors));
  const bits = [pub.journal, pub.volume, pub.pages].filter(Boolean);
  const venue = el("p", "venue", `${bits.join(", ")}${bits.length ? " " : ""}(${pub.year})`);
  const links = el("div", "citation-links");
  const candidates = [["DOI", pub.doi], ["Journal", pub.journal_url], ["arXiv", pub.arxiv], ["PDF", pub.pdf]];
  candidates.filter(([, url]) => url).forEach(([label, url]) => {
    const link = el("a", "", label); link.href = url; link.target = "_blank"; link.rel = "noopener noreferrer"; links.append(link);
  });
  article.append(heading, authors, venue);
  if (links.childElementCount) article.append(links);
  return article;
}

function renderSelected(publications, target) {
  target.replaceChildren(...publications.filter(pub => pub.selected).map(publicationEntry));
}

function renderAll(publications, target) {
  const byYear = Map.groupBy ? Map.groupBy(publications, pub => pub.year) : publications.reduce((map, pub) => map.set(pub.year, [...(map.get(pub.year) || []), pub]), new Map());
  const groups = [];
  byYear.forEach((items, year) => {
    const section = el("section", "year-group");
    const heading = el("h2", "", String(year)); heading.id = `year-${year}`;
    const list = el("div", "publication-list"); list.append(...items.map(publicationEntry));
    section.setAttribute("aria-labelledby", heading.id); section.append(heading, list); groups.push(section);
  });
  target.replaceChildren(...groups);
}

async function initPublications() {
  const selected = document.querySelector("#selected-publications");
  const all = document.querySelector("#all-publications");
  if (!selected && !all) return;
  try {
    const response = await fetch("data/publications.json");
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const publications = (await response.json()).sort((a, b) => b.year - a.year || a.title.localeCompare(b.title));
    if (selected) renderSelected(publications, selected);
    if (all) renderAll(publications, all);
  } catch (error) {
    const target = selected || all; target.replaceChildren(el("p", "error", "The publication list could not be loaded."));
    console.error(error);
  }
}

document.querySelectorAll(".nav-toggle").forEach(button => button.addEventListener("click", () => {
  const menu = document.getElementById(button.getAttribute("aria-controls"));
  const open = button.getAttribute("aria-expanded") === "true";
  button.setAttribute("aria-expanded", String(!open)); menu.classList.toggle("open", !open);
}));
document.getElementById("year").textContent = new Date().getFullYear();
initPublications();
