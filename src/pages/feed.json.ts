import { SITE } from '../config';

export async function GET() {
  const homePageUrl = 'https://teimakes.github.io/personal-blog/';
  const postImportResult = import.meta.glob('./posts/*.{md,mdx}', { eager: true });
  const posts = Object.values(postImportResult);
  const sorted = posts
    .filter((p: any) => !p.frontmatter.draft)
    .sort((a: any, b: any) => new Date(b.frontmatter.date) - new Date(a.frontmatter.date));

  return new Response(
    JSON.stringify({
      version: 'https://jsonfeed.org/version/1',
      title: SITE.title,
      home_page_url: homePageUrl,
      feed_url: new URL('feed.json', homePageUrl).href,
      description: 'Notes on AI, LLMs, AI Agents, AI movies, animation and manga.',
      items: sorted.map((p: any) => ({
        id: new URL(p.url, homePageUrl).href,
        url: new URL(p.url, homePageUrl).href,
        title: p.frontmatter.title,
        date_published: new Date(p.frontmatter.date).toISOString(),
        tags: p.frontmatter.tags,
      })),
    }),
    { headers: { 'Content-Type': 'application/json' } }
  );
}
