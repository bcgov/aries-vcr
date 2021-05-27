# Running Aries VCR

## How can I run Aries VCR?

You need to have a local Indy network running, you can use VON Network which is available here: https://github.com/bcgov/von-network

```
git clone https://github.com/bcgov/von-network.git
cd von-network
./manage build
./manage start
```

Once this is running, simply clone, build and run Aries VCR as follows:

```
https://github.com/bcgov/aries-vcr
cd aries-vcr/docker
./manage build
./manage start seed=my_seed_000000000000000000000123
```

## Is there a demo Issuer available?

There is a demo Issuer available here:  https://github.com/bcgov/aries-vcr-issuer-controller

There is also a more robust Issuer available here:  https://github.com/bcgov/von-bc-registries-agent

## How can I run Aries VCR from my own fork?

You will need your own fork if you intend to:

- Customize the Aries VCR code
- Update the code (fix bugs, add features) that you intend to submit back to bcgov

Simply fork the https://github.com/hyperledger/aries-vcr repository on github to create your own fork.

When you create a local clone, add the bcgov repo as an "upstream" as follows:

```
https://github.com/<you>/aries-vcr
cd aries-vcr
git remote add upstream https://github.com/hyperledger/aries-vcr
git remote -v
```

Depending on how much you customize Aries VCR code, you can keep your own fork up-do-date as follows:

```
git fetch upstream
git merge upstream/master
```

If you made any changes to core code, you may have to manually resolve conflicts.

## How can I customize Aries VCR?

### Customizing the User Interface

There is currently a basic Angular application
([Aries-VCR Client](https://github.com/bcgov/aries-vcr-client)) that offers a front-end UI for
Aries-VCR. Feel free to fork the repo and make changes to it as you see fit. Some examples of
custom implementations include: [OrgBook BC](https://github.com/bcgov/orgbook-bc-client) and
[OrgBook ON](https://github.com/bcgov/orgbook-on-client).

### Customizing the Back-end Python Code

There is a "custom theme" file for the back-end Python code, examples are:

- app/app/custom_settings_bcgov.py
- app/app/custom_settings_ongov.py

Just name your file "app/app/custom_settings_<theme>.py"

Build Aries VCR as follows (use your theme name):

```
THEME=bcgov ./manage build
THEME=bcgov ./manage start seed=my_seed_000000000000000000000123
```

Custom settings are loaded from "app/settings.py" (search for "custom_settings_file").

There is some code in "api_v2/utils.py" that you can use to get custom settings (from your own code).

### Adding a new Web Service

Updates to the back-end to add a new web service:

1. Add/update any models as required, and then generate migrations
2. Add/update serializers (based on the output format of the new services)
3. Add a view to support the service
4. Add a URL
5. See documentation around the "custom Python behaviour" code
6. Not sure if the openapi.yml file is acually used ...

Updates to the front end to consume the service (Note: this only applies if you are implementing
your UI based off of [Aries-VCR Client](https://github.com/bcgov/aries-vcr-client)):

1. Add a mapping for the service output data to data-types.ts
2. Shouldn't need to update general-data.service.ts
3. Update html and typescript as necessary to consume the new service and display the results