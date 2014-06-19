from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect
from django.contrib.messages.api import get_messages

from social_auth import __version__ as version

# Create your views here.

group_org = 7908743 # The organization number of the Github org. DOn't know how to find this form the web interface, sorry.
base_domain = 'ipython.sandiegodata.org'

def home(request):
    """Home view, displays login mechanism"""
    if request.user.is_authenticated():
        return HttpResponseRedirect('done')
    else:
        return HttpResponseRedirect('/login/github/')

@login_required
def done(request,  *args, **kwargs):
    """Login complete view, displays user data"""
    import logging

    import github  #pygithub
    from social_auth.models import UserSocialAuth
    from django.contrib.auth.models import User
    import ipydoc
    from ipydoc.manager import DockerManager, RedisManager, Director

    logger = logging.getLogger('views')

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

    # Now we can startup the container for the user.
    redis = RedisManager(ipydoc.ProxyConfig('ipython.sandiegodata.org', '192.168.1.30'),
                         'hipache')

    docker = DockerManager(ipydoc.DockerClientRef('tcp://192.168.1.30:4243', '1.9', 10), 'ipython')

    d = Director(docker, redis)


    password = d.start(django_user.username, repo_url, auth)

    logger.info(django_user.username + " " + password)

    ctx = {
        'password': password,
        'username': django_user.username,
        'host': 'http://{}.{}'.format(django_user.username, base_domain)
    }

    return render_to_response('done.html', ctx, RequestContext(request))


def logout(request):
    """Logs out user"""
    auth_logout(request)
    return HttpResponseRedirect('/')