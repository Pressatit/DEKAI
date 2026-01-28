import asyncio
import os
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode
from crawl4ai.content_filter_strategy import PruningContentFilter
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator
from urllib.parse import urlparse
async def main():
    # 1. Setup the "Knowledge Base" directory
    output_dir = "First year"
    os.makedirs(output_dir, exist_ok=True)
    

    # 2. Configure the Browser (Headless = Fast)
    custom_ua = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/130.0.0.0 Safari/537.36 "
    "(compatible; DekaiProject/1.0; student-research)"
)


    browser_config = BrowserConfig(
        headless=True, 
        verbose=True,
        user_agent=custom_ua,
        enable_stealth=True)

    # 3. Configure the "Cleaner" (Removes navigation/junk)
    md_generator = DefaultMarkdownGenerator(
        content_filter=PruningContentFilter(threshold=0.4, threshold_type="fixed")
    )

    # 4. Global Run Configuration
    run_config = CrawlerRunConfig(
        cache_mode=CacheMode.BYPASS,
        markdown_generator=md_generator
    )

    #
    urls = [
       "https://library.dkut.ac.ke/"
  
    ]

    async with AsyncWebCrawler(config=browser_config) as crawler:
        for url in urls:
            print(f"--- Crawling: {url} ---")
            url=url.strip()
            result = await crawler.arun(url=url, config=run_config)

            if result.success:
               
                # Get the cleaned "fit_markdown"
                content = result.markdown.fit_markdown
                
                parsed_url = urlparse(url)
                 # Get the 'netloc' (e.g., 'soe.dkut.ac.ke')
                domain_parts = parsed_url.netloc.split('.')
    
                  # Construction: Use the subdomain if it exists, otherwise use the main domain
                if len(domain_parts) > 2:
                   # e.g., 'soe_dkut'
                 filename = f"{domain_parts[0]}_{domain_parts[1]}.md"
                else:
                 filename = f"{domain_parts[0]}.md"

                print(f"Constructed Filename: {filename}")
                
                #filename="chaplaincy_dkut.md"
                #filename = url.split("/")[-1].replace(".php", "").replace("-", "_") + ".md"
                with open(os.path.join(output_dir, filename), "w", encoding="utf-8") as f:
                    f.write(content)
                
                print(f"✅ Saved to {output_dir}/{filename}")
            else:
                print(f"❌ Failed: {result.error_message}")

            # Politeness delay (essential for university sites!)
            await asyncio.sleep(5)

if __name__ == "__main__":
    asyncio.run(main())