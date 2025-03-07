default persistent.first_run = True


init 999 python:

    def random_chat():

        fae_random_chat_rate.adjustRandFrequency(persistent._fae_random_chat_freq)

define FAE_PRONOUN_GENDER_MAP = {
    "his": {"M": "his", "F": "her", "X": "their"},
    "he": {"M": "he", "F": "she", "X": "they"},
    "hes": {"M": "he's", "F": "she's", "X": "they're"},
    "heis": {"M": "he is", "F": "she is", "X": "they are"},
    "bf": {"M": "boyfriend", "F": "girlfriend", "X": "partner"},
    "man": {"M": "man", "F": "woman", "X": "person"},
    "boy": {"M": "boy", "F": "girl", "X": "person"},
    "guy": {"M": "guy", "F": "girl", "X": "person"},
    "him": {"M": "him", "F": "her", "X": "them"},
    "himself": {"M": "himself", "F": "herself", "X": "themselves"},
    "hero": {"M": "hero", "F": "heroine", "X": "hero"}
}

init python:

    import subprocess
    import os
    import re
    import store.fae_globals as fae_globals
    process_list = []
    currentuser = None

    if renpy.windows:
        try:
            process_list = subprocess.check_output("wmic process get Description", shell=True).lower().replace("\r", "").replace(" ", "").split("\n")
        except:
            pass
        
        try:
            for name in ('LOGNMAE', 'USER', 'LNAME', 'USERNAME'):
                user = os.environ.get(name)
                if user:
                    currentuser = user
        except:
            pass
    
    if not currentuser or len(currentuser) == 0:
        currentuser = persistent.playername
    if not persistent.mcname or len(persistent.mcname) == 0:
        persistent.mcname = currentuser
        mcname = currentuser
    
    else:
        mcname = persistent.mcname
    

    def fae_getuser():

        for name in ('LOGNAME', 'USER', 'LNAME', 'USERNAME'):
            user = os.environ.get(name)
            if user:
                return user
        return None

    def reveal():

        renpy.show("sayori idle", at_list=[t11], zorder=store.fae_sprites.FAE_SAYORI_ZORDER)
        
        renpy.hide("black")
    
    def fae_set_pronouns(key=None):
        """
        Sets gender specific word replacements

        Few examples:
            "It is his pen." (if the player's gender is declared as male)
            "It is her pen." (if the player's gender is declared as female)
            "It is their pen." (if player's gender is not declared)

        For all available pronouns/words check the keys in FAE_PRONOUN_GENDER_MAP

        IN:
            key - Optional[Literal["M", "F", "X"]] - key (perhaps current gender) to set the pronouns for
                If None, uses persistent.gender
        """
        store = renpy.store

        if key is None:
            key = store.persistent.gender

        for word, sub_map in store.FAE_PRONOUN_GENDER_MAP.items():
            if key in sub_map:
                value = sub_map[key]
            else:
                value = sub_map["X"]
            setattr(store, word, value)
        

label ch30_main:

    $ quick_menu = True

    if not config.developer:
        $ style.say_dialogue = style.normal
    
    $ s_name = persistent._fae_sayori_nickname

    if not persistent.fae_intro_complete:
        jump fae_intro_checks
    else:
        jump ch30_setup


label ch30_autoload:

    if fae_is_evening():
        play music s1
    
    if not fae_is_day() and not fae_is_evening():
        play music s2
    

    scene black


    python:
        quick_menu = True
        style.say_dialogue = style.normal
        
        if not config.developer:
            config.allow_skipping = False
    
    $ store.fae_utilities.makedirifnot("{0}/gifts/".format(renpy.config.basedir))

    $ fae_set_pronouns()

    if not persistent.games_reset:
        $ ResetGames()
      
    jump ch30_main


    #FALL THROUGH
    
label ch30_setup:

    #SET UP BG AND STUFF BEHIND A BLACK SCREEN

    show black zorder 99

    python:
        main_background.form()

        fae_atmosphere.showSky(fae_atmosphere.WEATHER_SUNNY, with_transition=False)
        
        Affection.checkResetDailyAffectionGain()
        fae_outfits.get_user_acs()
        fae_outfits.call_user_outfit()
        fae_outfits.FAEAcs.call_all()
        fae_outfits.FAEOutfit.call_all()
        fae_utilities.log("Outfit data loaded.")
        if fae_outfits.outfit_exists(persistent.fae_outfit_quit):
            Sayori.setOutfit(fae_outfits.get_outfit(persistent.fae_outfit_quit))
        else:
            Sayori.setOutfit(fae_outfits.get_outfit("fae_uniform"))

        try:
            setupRPC("In the spaceroom")
        except:
            pass
    
        random_chat()

    #FALL THROUGH

label fae_event_check:

    if fae_isPlayerBday():
        jump fae_player_bday_autoload
        

    if fae_isO31():
        jump fae_o31_autoload
        
    
    if fae_isD25():
        $ fae_outfits.get_acs("fae_scarf").unlock()
        $ fae_outfits.get_outfit("fae_christmas").unlock()
        $ Sayori.setOutfit(fae_outfits.get_outfit("fae_christmas"))
        jump fae_d25_autoload
    
    if fae_isF14():
        jump fae_f14_autoload
        
    
    if fae_isNYD():
        jump fae_nyd_autoload

    else:
        $ holidayReset()
    
label ch30_init:

    $ persistent.fae_sayori_closed = False

    $ persistent.autoload = "ch30_autoload"

    python:
        _fae_AffStart()
        import random

        
        Affection.checkResetDailyAffectionGain()

        Sayori.setInChat(True)

        if store.persistent._fae_absence_choice is not None:
            persistent.fae_visit_counter += 1
            persistent.fae_last_visit_date = datetime.datetime.now()
            ats("s_greeting_long_away")
            reveal()
            renpy.jump("cnc")

        if (datetime.datetime.now() - persistent.fae_last_visit_date).total_seconds() / 604800 >= 2 and persistent._fae_absence_choice is None:
            Sayori.add_regret_quit(fae_regrets.RegretTypes.long_absence)
        
        elif not persistent._fae_player_apology_type_on_quit:
            Affection.calculatedAffectionGain()
            
        persistent.fae_visit_counter += 1
        persistent.fae_last_visit_date = datetime.datetime.now()

        fae_outfits.get_user_acs()
        fae_outfits.call_user_outfit()
        fae_outfits.FAEAcs.call_all()
        fae_outfits.FAEOutfit.call_all()
        fae_utilities.log("Outfit data loaded.")

        if fae_outfits.outfit_exists(persistent.fae_outfit_quit):

            Sayori.setOutfit(fae_outfits.get_outfit(persistent.fae_outfit_quit))
        
        else:
            Sayori.setOutfit(fae_outfits.get_outfit("fae_uniform"))
        
        fae_utilities.log("Outfit Set.")
        
        fae_events.EVENT_RETURN_OUTFIT = fae_outfits.get_outfit(store.persistent.fae_outfit_quit)
            
        
        if not cielp("^greeting_"):

            if (
                random.randint(0, 16) == 1
                and (not persistent.fae_mood_on_quit and not persistent._fae_player_apology_type_on_quit)
                and fae_events.event_selector()
            ):
                ats(fae_events.event_selector())
                renpy.call("cnc", False)
            
            else:
                try:
                    ats(fae_greetings.greet_sel())
                except:
                    ats("s_greeting_5")
                persistent.fae_mood_on_quit = None
                persistent._fae_player_apology_type_on_quit = None
                reveal()
                renpy.call("cnc")
                
    
    show sayori idle at t11 zorder store.fae_sprites.FAE_SAYORI_ZORDER
    hide black with Dissolve(2)
    show screen hidden1(True)

    #FALL THROUGH
label after_holiday:

    pass

label ch30_loop:

    $ init_qabs()

    show sayori idle at fae_center zorder store.fae_sprites.FAE_SAYORI_ZORDER

    show screen hidden1(True)

    python:

        _present = datetime.datetime.now()

        if PRIOR_CHECK_MINUTELY.minute is not _present.minute:
            minute_check()
            PRIOR_CHECK_MINUTELY = _present

            if PRIOR_CHECK_MINUTELY.minute in (0, 15, 30, 45):
                qh_check()
            
            if PRIOR_CHECK_MINUTELY.minute in (0, 30):

                hh_check()
            
        if PRIOR_CHECK_HOURLY is not _present.hour:
            h_check()
            PRIOR_CHECK_HOURLY = _present.hour
        
        if PRIOR_CHECK_DAILY is not _present.day:
            d_check()
            PRIOR_CHECK_DAILY = _present.day
        
        Sayori.setInChat(False)

    $ fae_random_chat_rate.wait()

    if not fae_random_chat_rate.waitedLongEnough():

        jump after_random_pick
    else:
        $ fae_random_chat_rate.setWaitingTime()
    
    
    label select_topic:

        while persistent._event_list:
            call cnc_notify(True)

label after_random_pick:

    $ _return = None

    show screen hidden1(True)

    jump ch30_loop




label cnc(show_sayori=True):

    $ remove_qabs()

    if show_sayori:
        show sayori idle at fae_center zorder fae_sprites.FAE_SAYORI_ZORDER

    if persistent._event_list:
        $ _chat = persistent._event_list.pop(0)

        if renpy.has_label(_chat):


            $ Sayori.setInChat(True)

            hide screen hidden1

            call expression _chat from _call_expression
    
    python:
        return_keys = _return if isinstance(_return, dict) else dict()

        chat_obj = get_chat(_chat)

        if chat_obj is not None:
            chat_obj.seen_no += 1
            chat_obj.latest_seen = datetime.datetime.now()

        if "derandom" in return_keys:
            chat_obj.random = False
        if "love" in return_keys:
            love()
    
    if "quit" in return_keys:
        $ persistent.fae_sayori_closed = True
        jump confirm_quit
    
    python:
        global LCC
        LCC = datetime.datetime.now()
        Sayori.setInChat(False)
    
    window hide

    show screen hidden1(True)

    jump ch30_loop

label cnc_notify(show_sayori=True):

    $ remove_qabs()

    if show_sayori:
        show sayori idle at fae_center zorder fae_sprites.FAE_SAYORI_ZORDER

    if persistent._event_list:
        $ _chat_notify = persistent._event_list.pop(0)

        if renpy.has_label(_chat_notify):

            if store.fae_notifs.can_show_notifs and persistent._fae_notifs_enabled:

                if renpy.windows:

                    $ fae_notifs.notifyWindows()
                
                elif renpy.linux:

                    $ fae_notifs.notifyLinux()

            $ Sayori.setInChat(True)

            hide screen hidden1

            call expression _chat_notify from _call_expression_10
    
    python:
        return_keys = _return if isinstance(_return, dict) else dict()

        chat_obj = get_chat(_chat_notify)

        if chat_obj is not None:
            chat_obj.seen_no += 1
            chat_obj.latest_seen = datetime.datetime.now()

            if "derandom" in return_keys:
                chat_obj.random = False
            if "love" in return_keys:
                love()
    
    if "quit" in return_keys:
        $ persistent.fae_sayori_closed = True
        jump confirm_quit
    
    python:
        global LCC
        LCC = datetime.datetime.now()
        Sayori.setInChat(False)
    
    window hide

    show screen hidden1(True)

    jump ch30_loop

label force_quit:

    if (
        fae_intro.FAEIntroStatus(persistent.fae_intro_status) == fae_intro.FAEIntroStatus.complete
        and fae_farewells.FAEForceQuitStates(persistent.fae_player_force_quit_state) == fae_farewells.FAEForceQuitStates.not_force_quit
    ):

        $ ats("farewell_force_quit")
        $ renpy.jump("cnc")
    
    elif not fae_intro.FAEIntroStatus(persistent.fae_intro_status) == fae_intro.FAEIntroStatus.complete:

        $ renpy.jump("confirm_quit")

    
    else:

        s ebgchga "YOU CAN'T LEAVE LIKE THAT!"

        python:
            Affection.percentageAffectionLoss(2)
            Sayori.add_new_regret_awaiting(fae_regrets.RegretTypes.unexpected_quit)
            Sayori.add_regret_quit(fae_regrets.RegretTypes.unexpected_quit)
        
        $ renpy.jump("confirm_quit")