import rss from '@astrojs/rss';
import { SITE } from '../config';

export async function GET(context) {
  const postImportResult = import.meta.glob('./posts/*.{md,mdx}', { eager: true });
  const posts = Object.values(postImportResult)
    .filter((p) => !p.frontmatter.draft)
    .sort((a, b) => new Date(b.frontmatter.date) - new Date(a.frontmatter.date));

  return rss({
    title: SITE.title,
    description: SITE.description,
    site: context.site,
    items: posts.map((p) => ({
      title: p.frontmatter.title,
      description: p.frontmatter.description,
      pubDate: new Date(p.frontmatter.date),
      link: p.url,
    })),
  });
}
