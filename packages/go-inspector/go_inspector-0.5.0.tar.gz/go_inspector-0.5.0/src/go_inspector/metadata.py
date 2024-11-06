# -*- coding: utf-8 -*-
#
# Copyright (c) nexB Inc. and others. All rights reserved.
# ScanCode is a trademark of nexB Inc.
# SPDX-License-Identifier: Apache-2.0
# See http://www.apache.org/licenses/LICENSE-2.0 for the license text.
# See https://github.com/nexB/go-inspector for support or download.
# See https://aboutcode.org for more information about nexB OSS projects.
#

import requests
from packageurl import PackageURL

from go_inspector import utils

"""
Fetch Go module metadata from the Go packages website
"""


def fetch_go_data(purl):
    """
    Return live PackageData for the Go package ``purl`` string or None.
    For exmaple:
    >>> pkg = fetch_go_data(purl="pkg:golang/github.com/jwells131313/goethe@v1.4.0")
    >>> pkg.extracted_license_statement
    'Apache-2.0, CDDL-1.1, GPL-2.0'
    """
    # Note: this is scraping the web page because there is no Go api.
    # See also https://api.deps.dev/v3alpha/purl/pkg:golang%2fgithub.com%2fjwells131313%2fgoethe@v1.4.0
    from packagedcode import models

    purl = PackageURL.from_string(purl)

    url = utils.repository_homepage_url(purl)
    try:
        resp = requests.get(url=url)
    except:
        return
    if not resp.status_code == 200:
        return

    extracted_license_statement = None
    homepage_url = None

    # the data has this shape:
    # <h2 class="go-textLabel">Repository</h2>
    # <div class="UnitMeta-repo">
    #
    #     <a href="https://github.com/jwells131313/goethe" title="https://github.com/jwells131313/goethe" target="_blank" rel="noopener">
    #       github.com/jwells131313/goethe
    #     </a>
    #
    # </div>
    # <span class="go-Main-headerDetailItem" data-test-id="UnitHeader-licenses">
    #     License:
    #         <span> Apache-2.0,  CDDL-1.1,  GPL-2.0</span>

    repo_is_next = False
    lic_is_next_next = False
    lic_is_next = False

    for line in resp.text.splitlines():
        line = line.strip()

        if not line:
            continue

        if '<div class="UnitMeta-repo">' in line:
            # next is href to "repository" homepage
            repo_is_next = True

        elif repo_is_next:
            #  <a href="https://github.com/jwells131313/goethe" title="https://github.com/jwells131313/goethe" target="_blank" rel="noopener">

            repo_is_next = False
            _, _, homepage_url = line.partition("href=")
            homepage_url = homepage_url.strip('"')
            homepage_url, _, _ = homepage_url.partition('"')

        elif 'data-test-id="UnitHeader-licenses"' in line:
            # next is license: and next, next are the license keys
            lic_is_next_next = True

        elif lic_is_next_next:
            lic_is_next_next = False
            lic_is_next = True

        elif lic_is_next:
            # <span> Apache-2.0,  CDDL-1.1,  GPL-2.0</span>
            lic_is_next = False
            extracted_license_statement = " ".join(
                line.replace("<span>", "").replace("</span>", "").strip().split()
            )

        if extracted_license_statement and homepage_url:
            break
    pkg_data = dict(
        extracted_license_statement=extracted_license_statement,
        homepage_url=homepage_url,
    )
    pkg_data.update(utils.get_urls(purl))
    pkg_data.update(purl.to_dict(encode=True, empty=None))
    return models.PackageData(**pkg_data)
