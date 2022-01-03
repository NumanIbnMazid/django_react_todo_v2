from django.views.generic import View
from django.shortcuts import render
import markdown
from pathlib import Path
import os
from django.conf import settings
from django.http import HttpResponse
import logging


class FrontendAppView(View):
    """
    Serves the compiled frontend entry point (only works if you have run `yarn
    run build`).
    """

    def get(self, request):
        try:
            with open(os.path.join(settings.REACT_APP_DIR, 'build', 'index.html')) as f:
                return HttpResponse(f.read())
        except FileNotFoundError:
            logging.exception('Production build of app not found')
            return HttpResponse(
                """
                This URL is only used when you have built the production
                version of the app. Visit http://localhost:3000/ instead, or
                run `yarn run build` to test the production version.
                """,
                status=501,
            )

class HomeView(View):
    
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return render(request, "index.html", context=context)

    def get_context_data(self, **kwargs):
        context = {}
        context["content"] = self.get_markdown_html()
        return context
    
    def get_project_readme_markdown(self):
        BASE_DIR = Path(__file__).resolve().parent.parent.parent
        readme_file = f"{BASE_DIR}/README.md"
        return readme_file
    
    def get_markdown_html(self):
        config = {
            'extra': {
                'footnotes': {
                    'UNIQUE_IDS': True
                },
                'fenced_code': {
                    'lang_prefix': 'lang-'
                }
            },
            'toc': {
                'permalink': True
            }
        }
        
        md = markdown.Markdown(extensions=['extra', 'toc'], extension_configs=config)
        
        html_data = None
        
        try:
        
            project_readme_file = self.get_project_readme_markdown()
            
            # Read readme file
            with open(project_readme_file, 'r') as readme_file:
                text = readme_file.read()
                html_data = md.convert(text)
        except Exception as E:
            html_data = str(E)
            
        return html_data
