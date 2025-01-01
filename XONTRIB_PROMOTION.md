## Xontrib Promotion (DO and REMOVE THIS SECTION)

-   Check that your repository name starts from `xontrib-` prefix. It helps Github search find it.

-   Add `xonsh`, `xontrib` and other thematic topics to the repository "About" setting.

-   Add preview image in "Settings" - "Options" - "Social preview". It allows to show preview image in Github Topics and social networks e.g. Twitter.

-   Enable "Sponsorship" in "Settings" - "Features" - Check "Sponsorships".

-   Add xontrib to the [awesome-xontribs](https://github.com/xonsh/awesome-xontribs).

-   Publish your xontrib to PyPi via Github Actions and users can install your xontrib via `xpip install xontrib-myxontrib`. Easiest way to achieve it is to use Github Actions. Register to https://pypi.org/ and [create API token](https://pypi.org/help/#apitoken). Go to repository "Settings" - "Secrets" and your PyPI API token as `PYPI_API_TOKEN` as a "Repository Secret". Now when you create new Release the Github Actions will publish the xontrib to PyPi automatically. Release status will be in Actions sction. See also `.github/workflows/release.yml`.

-   Write a message to: [xonsh Gitter chat](https://gitter.im/xonsh/xonsh?utm_source=xontrib-template&utm_medium=xontrib-template-promo&utm_campaign=xontrib-template-promo&utm_content=xontrib-template-promo), [Twitter](https://twitter.com/intent/tweet?text=xonsh%20is%20a%20Python-powered,%20cross-platform,%20Unix-gazing%20shell%20language%20and%20command%20prompt.&url=https://github.com//xontrib-pygitstatus), [Reddit](https://www.reddit.com/r/xonsh), [Mastodon](https://mastodon.online/).
