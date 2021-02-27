# Mousehunt

Python scripts for making our mouse hunting lives easier. A few selected hunting locations have been built due to the additional human-input requirement during hunting.

Run the script in virtual environment for testing purposes. It will need to be executed as cron job to successfully trigger its functions. 

# Disclaimer

Note that using the bot to automate any processes is against the Mousehunt's gameplay rules and may result in the termination of the account. We do not take any responsibilities if your account has been impacted by using the following scripts.

This project is intended for hobby and coding practices only.

# Quick Overview

To use this application, make sure you have python 3 installed on your computer. Install virtual environment and the additional dependencies.

```
python app.py
```

Execute the application by running app.py. You will need to update the file with your login token.

```
config1 = {
    "login_token": [YOUR TOKEN HERE]
}

```

The following hunting locations have been built

-   Bristle Woods Rift
-   Floating Islands

Execute the code with:

```
mh = MouseHunt(user)
mh.automateHunt()

```

# Detailed Usage

## Step 1 - Creating Virtual Environmnet

Install python 3 on your computer, any python3 version should run the code without problems.

If you have not installed virtualenv, install by by executing `pip install virtualenv`

Create python virtual environment by executing the following codes

```
virtualenv venv
venv/Scripts/activate

```

## Step 2 - Accessing Token and Unique Hash

After logging into mousehunt, press F12 to access development tab. Click on 'camp' to trigger a round of data retrieval from server. Retrieve the token and unique hash as shown below.

This is the location of token, it is stored as a cookie.
![Image of token](https://raw.githubusercontent.com/howardlhw/Mousehunt/master/images/token.png)

## Step 3 - Configuring app.py

Use a text editor to edit app.py. Update the token, and unique hash.

```
user = {
    'login_token': [YOUR TOKEN HERE]
}
```

## Step 4 - Executing script

Update the following section with the updated codes. The instance will run automatically when automateHunt is called. The parameters of automate hunt to pass into can be found in the respective sections.

You can execute this script by entering `python app.py`

```
def executeScript():
    while True:
        mh = MouseHunt(user)
        mh.automateHunt()
        time.sleep(120)

if __name__ == "__main__":
    executeScript()
```

# Quest Files

This section will elaborate in detail the configurations required to use the quest files.


## Bristle Woods Rift

In Bristle Woods Rift, user input is required for the following actions.

1. Toggling of Quantum Quarts
2. Chance of Traps
3. Change of Cheese
4. Portal selection
5. Scramble portals

The algorithm is designed to optimize cost and maximize yield. It is recommended to have at least 40 Quantum Quarts and 10 Portal Scramblers (option) to use the script. If the portal scramblers are running dangerously low, it will stop using portal scramblers.

The script will automatically convert ancient string cheese potions (using brie string cheese) and runic string cheese potions. It will also purchase brie string cheese automatically from shop if the brie string cheese is running low.

It currently does not intend to purchase portal scrambers from marketplace automatically.

**Configure Trap Setup in each chamber**

User can configure the loadout for each room by editing the loadout/bristleWoodsRiftLoadout.py. You can also use the default configuration.

```
'security_chamber': {
    'quantumQuarts': True,
    'bait': 'magical_string_cheese',
    'trinket': 'rift_vacuum_trinket'
}
```

Due to the challenges in dealing with mobile app specific backend, an additional library has been added
to parse the inputs. Please make sure that you have selected the input from the trap libraries. 

The following choices of bait and charma are available:
Cheese Options (bait)

-   brie_string_cheese
-   runic_string_cheese
-   ancient_string_cheese

Charm Options (trinket)

-   rift_vacuum_trinket
-   super_rift_vacuum_trinket

The chambers are selected automatically based on the user's item count.


## Floating Islands

On Floating Islands, it is assumed that the user has more than sufficient cyclone stone and bottled
wind for completion of run. The algorithm is designed such that:

1. On low altitude islands, cyclone stone is used until the first block is a shrine, prioritizing speed
2. On high altitude island, cyclone stone is used until there are 3 loot blocks, prioritizing hunts
3. On low altitude islands, depart after fully exploring the island.
4. On high altitude islands, do not depart until the island is full explored (kicked back to launchpad)
5. Never stay on launchpad to farm cloud curds

