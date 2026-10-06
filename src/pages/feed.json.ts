export async function GET() {
  const postImportResult = import.meta.glob('./posts/*.{md,mdx}', { eager: true });
  const posts = Object.values(postImportResult);
  const sorted = posts
    .filter((p: any) => !p.frontmatter.draft)
    .sort((a: any, b: any) => new Date(b.frontmatter.date) - new Date(a.frontmatter.date));

  return new Response(
    JSON.stringify({
      version: 'https://jsonfeed.org/version/1',
      title: 'AI Notebook',
      home_page_url: 'https://kofboy2000.github.io/personal-blog',
      feed_url: 'https://kofboy2000.github.io/personal-blog/feed.json',
      description: 'Notes on AI, LLMs, AI Agents, AI movies, animation and manga.',
      items: sorted.map((p: any) => ({
        id: 'https://kofboy2000.github.io/personal-blog' + p.url,
        url: 'https://kofboy2000.github.io/personal-blog' + p.url,
        title: p.frontmatter.title,
        date_published: new Date(p.frontmatter.date).toISOString(),
        tags: p.frontmatter.tags,
      })),
    }),
    { headers: { 'Content-Type': 'application/json' } }
  );
}
