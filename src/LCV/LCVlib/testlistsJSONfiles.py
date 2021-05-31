'''
* SPDX-FileCopyrightText: 2021 Michele Scarlato <michele.scarlato@endocode.com>
*
* SPDX-License-Identifier: MIT
'''


def JSONPathList():
    JSONPath = list()
    # hope-boot is license compliant
    JSONPath.append('json/hope-boot.json')

    # spotify-docker-maven-plugin uses only Apache 2.0, so it is compliant
    JSONPath.append('json/spotify-docker-maven-plugin.json')

    # spotify:dockerfile-maven-plugin uses only Apache 2.0, so it is compliant
    JSONPath.append('json/dockerfile-maven.json')

    # ffabric8io-docker-maven-plugin uses only Apache 2.0, so it is compliant
    JSONPath.append('json/fabric8io-docker-maven-plugin.json')
    # emptyJSON

    # This project does not specify correctly an SPDX id for its oubound license
    JSONPath.append('json/javacv.json')

    # This project does not specify correctly an SPDX id for its oubound license
    JSONPath.append('json/javacpp.json')

    # GPL-3.0-or-later is not supported, because 'or later' notation.
    JSONPath.append('json/TelegramBots.json')

    # 1 above 3 licenses found are compatible.
    JSONPath.append('json/git-commit-id-maven-plugin.json')

    # An UNKNOWN license has been found within the project. This cannot reveal license incompatibility
    JSONPath.append('json/teamspeak3.json')

    # 9
    # outbound Apache2.0 https://github.com/dzikoysk/reposilite
    JSONPath.append('json/org.panda-lang:reposilite.json')

    # policeman-tools/forbidden-apis
    # outbound Apache2.0 https://api.github.com/repos/policeman-tools/forbidden-apis/license

    # 10 https://github.com/mojohaus/versions-maven-plugin
    # JSONPath.append('json/policeman-tools-forbidden-apis.json')
    JSONPath.append('json/org.codehaus.mojo:versions-maven-plugin.json')

    # 11  https://github.com/revelc/formatter-maven-plugin
    JSONPath.append(
        'json/net.revelc.code.formatter:formatter-maven-plugin.json')

    # 12
    JSONPath.append(
        'json/com.github.jhg023:SimpleNet.json')

    # 13
    JSONPath.append(
        'json/com.github.cryptomorin:XSeries.json')

    # 14
    JSONPath.append(
        'json/org.codehaus.mojo:exec-maven-plugin.json')

    # 15
    JSONPath.append(
        'json/org.codehaus.mojo:flatten-maven-plugin.json')

    # 16
    JSONPath.append(
        'json/org.sonarsource.scanner.maven:sonar-maven-plugin.json')
    # 17
    JSONPath.append(
        'json/spring-cloud-build.json')
    # 18
    JSONPath.append(
        'json/java-comment-preprocessor.json')
    # 19
    JSONPath.append(
        'json/gitflow-helper-maven-plugin.json')
    # 20
    JSONPath.append(
        'json/appassembler.json')

    # 21
    JSONPath.append(
        'json/aspectj-maven-plugin.json')
    # 22
    JSONPath.append(
        'json/jaxb2-maven-plugin.json')
    # 23
    JSONPath.append(
        'json/radar-covid-backend-configuration-server.json')
    # 24
    JSONPath.append(
        'json/reproducible-build-maven-plugin.json')
    # 25
    JSONPath.append(
        'json/rpm-maven-plugin.json')
    # 26
    JSONPath.append(
        'json/buildnumber-maven-plugin.json')
    # 27
    JSONPath.append(
        'json/Simple-YAML.json')
    # 28
    JSONPath.append(
        'json/cyclonedx-maven-plugin.json')
    # 29
    JSONPath.append(
        'json/rpm-builder.json')
    # 30
    JSONPath.append(
        'json/executable-jar-with-maven-example.json')
    # 31
    JSONPath.append('json/webdrivermanager.json')

    return JSONPath
