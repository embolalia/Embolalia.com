Title: Markdown in Docstrings (finally)
Date: 2013-8-11 12:10:36

[Willie](http://willie.dftba.net) has been mixing Markdown and ReStructuredText
in its documentation for some time. I found it was easier to use Markdown for
the automatically generated wiki pages than to use ReST (although, really,
Markdown is just about *always* easier to use than ReST), so all the modules
used Markdown in their documentation. But since we use
[Sphinx](http://sphinx-doc.org/) to generate the API docs, and Sphinx only does
ReST, that some files had ReST docs and some had Markdown. No longer. Thanks to
a quick and dirty hack, we can send the docstrings through Pandoc to translate
them from Markdown to ReST. Now, only the overall template has to be written in
ReST, while the vast majority of the documentation can be written in the much
easier Markdown.

From [Ducking](http://duckduckgo.com) about trying to find a solution to this,
it seems there are a lot of people who want this, but nobody else has published
a solution. I've put my hack up on
[GitHub](https://github.com/embolalia/Sphinx-Pandoc), so hopefully people will
find some use for it. Maybe at some point I'll be motivated to create a Sphinx-
like tool that uses Markdown through-and-through…
