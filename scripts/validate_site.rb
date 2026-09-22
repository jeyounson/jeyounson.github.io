# frozen_string_literal: true

require 'json'
require 'nokogiri'
require 'pathname'
require 'uri'
require 'yaml'

root = Pathname.new(__dir__).parent
site = root.join('_site')
failures = []
check = ->(condition, message) { failures << message unless condition }
pages = ['index.html', 'teaching/index.html', '404.html'] + Dir.glob(root.join('_site/{research,essays}/**/index.html')).map { |path| Pathname.new(path).relative_path_from(site).to_s }
documents = {}

pages.each do |path|
  file = site.join(path)
  check.call(file.file?, "Missing page: #{path}")
  next unless file.file?
  doc = Nokogiri::HTML(file.read)
  documents[path] = doc
  check.call(doc.css('main#main-content').length == 1, "Main landmark: #{path}")
  check.call(doc.at_css('nav[aria-label="Main navigation"]'), "Navigation landmark: #{path}")
  check.call(doc.at_css('a.skip-link[href="#main-content"]'), "Skip link: #{path}")
  check.call(doc.at_css('link[rel="canonical"]')['href'].start_with?('https://www.jeyounson.com/'), "Canonical host: #{path}")
  ids = doc.css('[id]').map { |node| node['id'] }
  check.call(ids.uniq.length == ids.length, "Duplicate IDs: #{path}")
  doc.css('script[type="application/ld+json"]').each { |node| JSON.parse(node.text) }
  doc.css('a[href], img[src], script[src], link[rel="stylesheet"]').each do |node|
    value = node['href'] || node['src']
    next if value.nil? || value.match?(%r{\A(?:[a-z]+:|//)}i)
    target_path, fragment = value.split('#', 2)
    target_path = URI::DEFAULT_PARSER.unescape(target_path.split('?', 2).first.to_s)
    target = if target_path.empty?
               file
             elsif target_path.start_with?('/')
               site.join(target_path.delete_prefix('/'))
             else
               file.dirname.join(target_path)
             end
    target = target.join('index.html') if target.directory?
    check.call(target.file?, "Broken local target in #{path}: #{value}")
    if fragment && !fragment.empty? && target.file? && target.extname == '.html'
      target_doc = target == file ? doc : Nokogiri::HTML(target.read)
      check.call(target_doc.css('[id]').any? { |element| element['id'] == fragment }, "Missing fragment in #{path}: #{value}")
    end
  end
end

home = documents.fetch('index.html')
papers = YAML.safe_load(root.join('_data/publications.yaml').read, permitted_classes: [Date], aliases: true).fetch('papers')
check.call(home.css('#publication-list .paper').length == papers.length, 'Publication inventory changed')
check.call(home.css('.filter-btn').all? { |node| node.name == 'button' && node.key?('aria-pressed') }, 'Category controls must be buttons')
check.call(home.css('.paper-abstract > summary').length == papers.count { |paper| paper['abstract_en'] }, 'Native abstracts missing')
teaching = documents.fetch('teaching/index.html')
check.call(teaching.at_css('a[href="https://deepwrite.jeyounson.com/workshops/"]'), 'Public workshop destination missing')
check.call(teaching.at_css('a[href="https://deepwrite.jeyounson.com/login"]'), 'Course login destination missing')
check.call(teaching.at_css('a[href="https://write.jeyounson.com/"]'), 'Verified archive destination missing')
check.call(!teaching.css('a[href]').any? { |a| a['href'].match?(%r{room\.jeyounson|/(staff|admin|assignments|feedback)}) }, 'Unexpected operational/private destination')
check.call(root.join('CNAME').read.strip == 'www.jeyounson.com', 'CNAME changed')
check.call(site.join('robots.txt').read.include?('Sitemap: https://www.jeyounson.com/sitemap.xml'), 'Robots sitemap host mismatch')
sitemap = Nokogiri::XML(site.join('sitemap.xml').read) { |config| config.strict }
check.call(sitemap.xpath('//*[local-name()="loc"]').all? { |node| node.text.start_with?('https://www.jeyounson.com/') }, 'Sitemap host mismatch')
%w[docs scripts orcid vendor].each { |path| check.call(!site.join(path).exist?, "Non-site directory published: #{path}") }

article = Nokogiri::HTML(site.join('assets/publications/legal-acts-agents-en/index.html').read)
check.call(article.at_css('link[rel="canonical"]')['href'] == 'https://www.jeyounson.com/assets/publications/legal-acts-agents-en/', 'Standalone article canonical mismatch')
check.call(article.at_css('meta[name="citation_pdf_url"]')['content'] == 'https://www.jeyounson.com/assets/publications/legal-acts-agents-en/index.pdf', 'Standalone article PDF metadata mismatch')
article.css('script[type="application/ld+json"]').each { |node| JSON.parse(node.text) }

abort(failures.join("\n")) unless failures.empty?
puts "PASS: #{pages.length} pages, #{papers.length} publications, local links/anchors, landmarks, JSON-LD, destinations, canonical/sitemap and output exclusions"
