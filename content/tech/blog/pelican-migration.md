Title: Migrating my site to Pelican
Summary: A Site Restructuring Adventure
Date: 2022-06-06
Tags: tech, how-to, python, pelican
Slug: pelican-migration

I recently came across a nice theme I liked in Hugo called [Dimension](https://github.com/your-identity/hugo-theme-dimension),
based on the responsive [html5up theme](https://html5up.net/dimension) of the same name.
The thing I liked most about the theme is how I could fix a big problem I had with my old site...
The old layout placed far too much emphasis on my tech skills, 
while barely mentioning my passion for [art](/art/index.html) and [music](/music/index.html).
I love the tech skills I have aquired over the years, and while coding
can be a creative outlet and mode of expression in some ways, 
I often feel more integrated and free when I am spending time at the piano or drawing.  

So I really liked the idea of what you see on my [homepage](/index.html) now,
but I quickly ran into problems trying to apply it to my site with hugo.
I recently spent a few weeks working on my web-chops, so I had some fresh html, CSS, and JS skills I was eager to apply.
And as it often ironically goes, [Hugo](https://gohugo.io/), 
the tool that got me off the ground quickly with a site, was now getting in the way.
In order to add serious customization to hugo, I would have to learn the go templating syntax and potentially some golang too.
I thought that might stretch my "learning new things-applying those things" loop way too wide, so I went with another option instead...

### Pelican to the rescue

I took a look at the current options for static site generation that Python has to offer and settled on [Pelican](https://blog.getpelican.com/).
With this I would only have the [jinja2](https://jinja.palletsprojects.com/) templating syntax to grapple with, something I had much more familiarity with.
And of course if I required any further customization (and I quickly found out I *would*), 
Pelican provides "sky's the limit" customization via their plugin interface, 
so with 11 years of off-and-on Python experience,
I was feeling pretty good about undergoing a bigger switch and migrating over.

### The real work was the customization

Migrating the content didn't really require anything, since Hugo and Pelican both can read markdown.
Some of my shortcodes didn't carry over from hugo, but it was pretty easy to replace that with the
[jinja2content](https://github.com/pelican-plugins/jinja2content) plugin instead.

The first wrinkle was the theme and styling.
Since Dimension is a single-page theme that assumes a fairly flat blog-style layout, 
it didn't have a good submenu option for listing article-style pages separately out of the box,
so I needed to add a #article-menu div for when I would need that.
I added supporting CSS that hooked into the existing stretching on page-load script and
had to wrestle with some alignment and padding issues:

```
#article-menu {
		display: -moz-flex;
		display: -webkit-flex;
		display: -ms-flex;
		display: flex;
		-moz-flex-direction: column;
		-webkit-flex-direction: column;
		-ms-flex-direction: column;
etc...
}
```

The second big problem was with Pelican itself.
Without a custom plugin, Pelican will flatten all the folders you identify as articles and pages.
While there is only one big article list, 
Pelican does include categories, tags, and pagination.
With these settings enabled, the site-builder will generate extra pages in order
to navigate a larger article list sensibly.

While you can tweak the save-as Pelican settings to get articles and pages to match their content-folder depth, 
in my case I needed Pelican to be able to sort and find only the articles and pages for the index.html it was building. 
I organized everything in my content folder before writing my plugin (see screenshot below).
I didn't want to have to reorganize how I wanted to think of my site,
just to fit Pelican's existing model.
So I realized I had to disable the existing article and page generators in Pelican for starters:

```
def disable_page_writing(generators):
    """
    Disable normal article and page generation.
    The html5up Dimension theme fits better as index pages.
    """
    def generate_output_override(self, _):
        if isinstance(self, ArticlesGenerator):
            log.debug('Skipping normal article generation...')
        if isinstance(self, PagesGenerator):
            log.debug('Skipping normal pages generation...')

    for generator in generators:
        if isinstance(generator, (ArticlesGenerator, PagesGenerator)):
            generator.generate_output = types.MethodType(generate_output_override, generator)

def register():
    signals.all_generators_finalized.connect(disable_page_writing)
```

Sticking with a layout that made sense *to me*, 
my content folder looks something like this:

![Content Directory](/images/posts/pelican-migration/dirlayout.png)

I am currently only using one layer of depth,
but my plugin will recognize an index file at any depth if I want to split it deeper in the future.
If a sub-interest starts to occupy a lot of my time, maybe I'll add a sub-*sub*-page, who knows.
Under the hood my plugin will use a recursive glob to find all the index files,
in my case set to index.md.
So my `/index.md` will generate `/index.html`, `/tech/index.md` will generate `/tech/index.html`, etc.

This fit pretty nicely with Dimension's single index.html design.
Once I had some code to gather the necessary articles for each,
my code can build everything it needs looping over the index file list.

So for right now I really only need four big index.html files: 
one at the root url in addition to the ones at `/art` `/music` and `/tech`.
Any pages in the same directory as that index file show as buttons,
and any articles at the same depth are listed in the article-menu.
The article and page paths are still specified by the standard Pelican settings.

The resulting code was a new generator that still leveraged [Pelican's
stock ArticleGenerator and PageGenerator](https://docs.getpelican.com/en/latest/internals.html#overall-structure)
for *reading* the article and page markdown content.
My plugin will prevent it from *generating* output under separate html files,
since it is coupled pretty tightly to the Dimension page design.

So to illustrate this, the location of `pelican-migration.md`, 
the post you are reading right now, is located in a path I have specified has articles in it: `tech/blog`.
So as the plugin is building `tech/index.html`, 
it includes a list of those post in the [tech](/tech/index.html) article menu,
and it also dumps in the content for that post as a #link,
hidden by Dimension's JS and CSS code until the user clicks it.

So it seemed fitting to name the class that does this IndexGenerator:

```
class IndexGenerator(Generator):
    def generate_context(self):
        """
        Find all index.{ext} files in content folder
        Add them to self.context['generated_content']
        """
        ...
    def generate_output(self, writer):
        """
        For each index page, generate index.html with 
        articles and pages at the same depth.
        """
        ...

def get_generators(pelican):
    return IndexGenerator

def register():
    signals.get_generators.connect(get_generators)
```

I'm glossing over the code here because there are quite a few lines, 
but you can look at the full source on [github](https://github.com/exvertus/thomasflanigan).
The two important hooks in Pelican generators are the generate_context and generate_output methods.
Pelican will not generate any output until all Generator class objects have finished generate_context.
This is how I am able to highjack generate_context code from the Article and Page Generators
without their generate_output methods creating the standard (in my case extra) articles and page output files.

While this felt like a bit of an adventure, I much happier landing with Pelican. 
The site-builder fits my content folder, not the other way around, but I didn't have to reinvent any wheels to get there either.
Pelican's plugin interface allowed me to pretty seamlessly use the pieces I needed and override what I did not.

### Next steps

I'll need to clean up a bit of code and rethink the settings a bit before I package this for general consumption,
but I've got shipping this work as separate projects on my to-do list so other Pelican users can use this plugin and theme too if they would like.

Pelican makes it pretty easy to ship Plugins as pip packages
and you can load themes in a similar way with 'pelican-themes --install'.
I will need to look into Poetry package manager first, and also tweak a few minor responsiveness issues I caused when I tweaked the Dimension theme (you may have noticed some). I'll have more details and a new post when I get there.
If you are interested in following for more, I will announce future posts to [my linkedin](https://www.linkedin.com/in/thomas-flanigan/).
