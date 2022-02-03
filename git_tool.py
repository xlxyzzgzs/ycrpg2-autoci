from git import Repo
from git.cmd import Git
from git.remote import FetchInfo
repo = Repo("./static")
repo.remote().push()
repo.is_dirty()
repo.remote().pull()
repo.commit()
