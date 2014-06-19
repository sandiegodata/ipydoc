from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.shortcuts import render_to_response


# Create your views here.

group_org = 7908743 # The organization number of the Github org. DOn't know how to find this form the web interface, sorry.
base_domain = 'ipython.sandiegodata.org'

def home(request):
    """Home view, displays login mechanism"""

    return render_to_response('home.html')


@login_required
def done(request,  *args, **kwargs):
    """Login complete view, displays user data"""
    import logging
    import github  #pygithub
    import zerorpc
    import os
    import urlparse
    from social_auth.models import UserSocialAuth
    from django.contrib.auth.models import User


    logger = logging.getLogger('views')
    logger.setLevel(logging.DEBUG)

    # The UID comes from the social_auth plugin; its the DJango user id.
    uid = request.session.get('_auth_user_id')

    # Shouldn't have to get both, but I don't know how to use Django queries correctly.
    user = UserSocialAuth.objects.select_related('user').get(provider='github',user_id=uid)
    django_user = User.objects.get(id=uid)

    # Determine if the user is in the right orgnaization, and puke if not.
    # Should have a better error message.
    auth = user.extra_data['access_token']
    gh  = github.Github(auth )

    authenticated = False
    for org in gh.get_user().get_orgs():
        if org.id == group_org:
            authenticated = True
            break

    if not authenticated:
        raise Exception("Not authenticated")

    # If the organization has a repo named after the user, use it otherwise, create it.
    repo_url = None
    for repo in org.get_repos():
        if repo.name == django_user.username:
            repo_url = repo.clone_url
            break

    if not repo_url:
        repo = org.create_repo(django_user.username, auto_init=True )
        repo_url = repo.clone_url

    # Call the director service to create the container
    c = zerorpc.Client()

    c.connect(os.getenv('DIRECTOR_PORT'))
    password = c.start(django_user.username, repo_url, auth)

    logger.info(django_user.username + " " + password)

    scheme = urlparse.urlparse(os.getenv('HTTP_REFERER'))[0]

    ctx = {
        'password': password,
        'username': django_user.username,
        'host': '{}://{}.{}'.format(scheme, django_user.username, base_domain)
    }

    logger.info(ctx)

    return render_to_response('done.html', ctx, RequestContext(request))


def logout(request):
    """Logs out user"""
    auth_logout(request)
    return HttpResponseRedirect('/')