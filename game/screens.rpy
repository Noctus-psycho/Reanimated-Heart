################################################################################
## Initialization
################################################################################

init offset = -1


################################################################################
## Styles
################################################################################

style default:
    properties gui.text_properties()
    language gui.language

style input:
    properties gui.text_properties("input", accent=True)
    adjust_spacing False

style hyperlink_text:
    properties gui.text_properties("hyperlink", accent=True)
    hover_underline True

style gui_text:
    properties gui.text_properties("interface")


style button:
    properties gui.button_properties("button")

style button_text is gui_text:
    properties gui.text_properties("button")
    yalign 0.5


style label_text is gui_text:
    properties gui.text_properties("label", accent=True)

style prompt_text is gui_text:
    properties gui.text_properties("prompt")


style bar:
    ysize gui.bar_size
    left_bar Frame("gui/bar/left.png", gui.bar_borders, tile=gui.bar_tile)
    right_bar Frame("gui/bar/right.png", gui.bar_borders, tile=gui.bar_tile)

style vbar:
    xsize gui.bar_size
    top_bar Frame("gui/bar/top.png", gui.vbar_borders, tile=gui.bar_tile)
    bottom_bar Frame("gui/bar/bottom.png", gui.vbar_borders, tile=gui.bar_tile)

style scrollbar:
    ysize gui.scrollbar_size
    base_bar Frame("gui/scrollbar/horizontal_[prefix_]bar.png", gui.scrollbar_borders, tile=gui.scrollbar_tile)
    thumb Frame("gui/scrollbar/horizontal_[prefix_]thumb.png", gui.scrollbar_borders, tile=gui.scrollbar_tile)

style vscrollbar:
    xsize gui.scrollbar_size
    base_bar Frame("gui/scrollbar/vertical_[prefix_]bar.png", gui.vscrollbar_borders, tile=gui.scrollbar_tile)
    thumb Frame("gui/scrollbar/vertical_[prefix_]thumb.png", gui.vscrollbar_borders, tile=gui.scrollbar_tile)

style slider:
    ysize gui.slider_size
    base_bar Frame("gui/slider/horizontal_[prefix_]bar.png", gui.slider_borders, tile=gui.slider_tile)
    thumb "gui/slider/horizontal_[prefix_]thumb.png"

style vslider:
    xsize gui.slider_size
    base_bar Frame("gui/slider/vertical_[prefix_]bar.png", gui.vslider_borders, tile=gui.slider_tile)
    thumb "gui/slider/vertical_[prefix_]thumb.png"


style frame:
    padding gui.frame_borders.padding
    background Frame("gui/frame.png", gui.frame_borders, tile=gui.frame_tile) 



################################################################################
## In-game screens
################################################################################


## Say screen ##################################################################
##
## The say screen is used to display dialogue to the player. It takes two
## parameters, who and what, which are the name of the speaking character and
## the text to be displayed, respectively. (The who parameter can be None if no
## name is given.)
##
## This screen must create a text displayable with id "what", as Ren'Py uses
## this to manage text display. It can also create displayables with id "who"
## and id "window" to apply style properties.
##
## https://www.renpy.org/doc/html/screen_special.html#say

screen say(who, what):
    style_prefix "say"

    window:
        id "window"

        if who is not None:

            window:
                id "namebox"
                style "namebox"
                text who id "who"

        text what id "what"


    ## If there's a side image, display it above the text. Do not display on the
    ## phone variant - there's no room.
    if not renpy.variant("small"):
        add SideImage() xalign 0.0 yalign 1.0


## Make the namebox available for styling through the Character object.
init python:
    config.character_id_prefixes.append('namebox')

style window is default
style say_label is default
style say_dialogue is default
style say_thought is say_dialogue

style namebox is default
style namebox_label is say_label


style window:
    xalign 0.5
    xfill True
    yalign gui.textbox_yalign
    ysize gui.textbox_height

    background Image("gui/textbox.png", xalign=0.5, yalign=1.0)

style namebox:
    xpos 240
    xanchor gui.name_xalign
    xsize 410
    ypos -85
    ysize 98

    background Frame("gui/namebox.png", gui.namebox_borders, tile=gui.namebox_tile, xalign=gui.name_xalign)
    padding gui.namebox_borders.padding

style say_label:
    properties gui.text_properties("name", accent=True)
    xalign 0.42
    yalign 0.43

style say_dialogue:
    properties gui.text_properties("dialogue")

    xpos 365
    xsize 1225
    ypos 0


## Input screen ################################################################
##
## This screen is used to display renpy.input. The prompt parameter is used to
## pass a text prompt in.
##
## This screen must create an input displayable with id "input" to accept the
## various input parameters.
##
## https://www.renpy.org/doc/html/screen_special.html#input

screen input(prompt):
    style_prefix "input"

    window:

        vbox:
            xalign gui.dialogue_text_xalign
            xpos gui.dialogue_xpos
            xsize gui.dialogue_width
            ypos gui.dialogue_ypos

            text prompt style "input_prompt"
            input id "input"

style input_prompt is default

style input_prompt:
    xalign gui.dialogue_text_xalign
    properties gui.text_properties("input_prompt")

style input:
    xalign gui.dialogue_text_xalign
    xmaximum gui.dialogue_width


## Choice screen ###############################################################
##
## This screen is used to display the in-game choices presented by the menu
## statement. The one parameter, items, is a list of objects, each with caption
## and action fields.
##
## https://www.renpy.org/doc/html/screen_special.html#choice

screen choice(items):
    style_prefix "choice"

    vbox:
        for i in items:
            textbutton i.caption action i.action


## When this is true, menu captions will be spoken by the narrator. When false,
## menu captions will be displayed as empty buttons.
define config.narrator_menu = True


style choice_vbox is vbox
style choice_button is button
style choice_button_text is button_text

style choice_vbox:
    xalign 0.5
    ypos 405
    xpos 1550
    yanchor 0.5

    spacing gui.choice_spacing

style choice_button is default:
    properties gui.button_properties("choice_button")

style choice_button_text is default:
    properties gui.button_text_properties("choice_button")


## Quick Menu screen ###########################################################
##
## The quick menu is displayed in-game to provide easy access to the out-of-game
## menus.

screen quick_menu():

    ## Ensure this appears on top of other screens.
    zorder 100

    if show_quick_menu:

        hbox:
            style_prefix "quick"

            xalign 0.5
            yalign 1.0

            imagebutton auto "gui/history_%s.png" xpos -0.45 ypos 1 focus_mask True action ShowMenu('history') activate_sound "audio/hover.mp3"
            imagebutton auto "gui/back_%s.png" xpos -0.4 ypos 1 focus_mask True action Rollback() activate_sound "audio/hover.mp3"
            imagebutton auto "gui/skip_%s.png" xpos -0.2 ypos 1 focus_mask True action Skip() alternate Skip(fast=True, confirm=True) activate_sound "audio/hover.mp3"
            imagebutton auto "gui/auto_%s.png" xpos 0 ypos 1 focus_mask True action Preference("auto-forward", "toggle") activate_sound "audio/hover.mp3"
            imagebutton auto "gui/save_%s.png" xpos 0.2 ypos 1 focus_mask True action ShowMenu('save') activate_sound "audio/hover.mp3"
            imagebutton auto "gui/qsave_%s.png" xpos 0.4 ypos 1 focus_mask True action QuickSave() activate_sound "audio/hover.mp3"
            imagebutton auto "gui/qload_%s.png" xpos 0.6 ypos 1 focus_mask True action QuickLoad() activate_sound "audio/hover.mp3"
            imagebutton auto "gui/quoptions_%s.png" xpos 0.8 ypos 1 focus_mask True action ShowMenu('preferences') activate_sound "audio/hover.mp3"


## This code ensures that the quick_menu screen is displayed in-game, whenever
## the player has not explicitly hidden the interface.
init python:
    config.overlay_screens.append("quick_menu")

default quick_menu = True

style quick_button is default
style quick_button_text is button_text

style quick_button:
    properties gui.button_properties("quick_button")

style quick_button_text:
    properties gui.button_text_properties("quick_button")


################################################################################
## Main and Game Menu Screens
################################################################################

## Navigation screen ###########################################################
##S
## This screen is included in the main and game menus, and provides navigation
## to other menus, and to start the game.
screen navigation_2():
    if main_menu:
        vbox:
            style_prefix "navigation"

            xpos 0.064
            ypos 0.017

            spacing gui.navigation_spacing

            imagebutton auto "gui/button/loadtab_%s.png" xpos 0.70 ypos 0.5 focus_mask True action ShowMenu("load")

            imagebutton auto "gui/button/abouttab_%s.png" xpos 0.7 ypos 0.9 focus_mask True action ShowMenu("about")
        
        vbox:
            style_prefix "navigation"

            xpos 0.762
            ypos 0.017

            spacing gui.navigation_spacing

            imagebutton auto "gui/button/settingstab_%s.png" xpos 0.76 ypos 0.2 focus_mask True action ShowMenu("preferences")
            imagebutton auto "gui/button/helptab_%s.png" xpos 0.76 ypos 0.5 focus_mask True action ShowMenu("help")


    else:
        
        vbox:
            style_prefix "navigation"

            xpos 0.064
            ypos 0.017

            spacing gui.navigation_spacing

        
            imagebutton auto "gui/button/historytab_%s.png" xpos 0.76 ypos 0.2 focus_mask True action ShowMenu("history")

            imagebutton auto "gui/button/savetab_%s.png" xpos 0.79 ypos -0.01 focus_mask True action ShowMenu("save")

            imagebutton auto "gui/button/loadtab_%s.png" xpos 0.78 ypos -0.2 focus_mask True action ShowMenu("load")

            imagebutton auto "gui/button/quittab_%s.png" xpos 0.79 ypos -0.4 focus_mask True action MainMenu()

        vbox:
            style_prefix "navigation"

            xpos 0.762
            ypos 0.017

            spacing gui.navigation_spacing

            imagebutton auto "gui/button/settingstab_%s.png" xpos 0.76 ypos 0.2 focus_mask True action ShowMenu("preferences")

            imagebutton auto "gui/button/notestab_%s.png" xpos 0.77 ypos -0.01 focus_mask True action ShowMenu("character_sheet")

            imagebutton auto "gui/button/inventorytab_%s.png" xpos 0.776 ypos -0.2 focus_mask True action ShowMenu("inventory_tab")

            
            if _in_replay:

                textbutton _("End Replay") action EndReplay(confirm=True)
            
            if renpy.variant("pc") or (renpy.variant("web") and not renpy.variant("mobile")):

                ## Help isn't necessary or relevant to mobile devices.
                imagebutton auto "gui/button/helptab_%s.png" xpos 0.778 ypos -0.4 focus_mask True action ShowMenu("help")

screen navigation():

    vbox:
        style_prefix "navigation"

        xpos gui.navigation_xpos
        yalign 0.5

        spacing gui.navigation_spacing

        if main_menu:

            #textbutton _("Start") action Start()

            imagebutton auto "gui/newgame_%s.png" xpos 270 ypos 10 focus_mask True action Jump('animation') hover_sound "audio/hover.mp3" activate_sound "audio/click.mp3"
            

        else:

            textbutton _("History") action ShowMenu("history")


            textbutton _("Save") action ShowMenu("save")

        #textbutton _("Load") action ShowMenu("load")
        imagebutton auto "gui/continue_%s.png" xpos 270 ypos 20 focus_mask True action ShowMenu("load") hover_sound "audio/hover.mp3" activate_sound "audio/click.mp3"



        #textbutton _("Preferences") action ShowMenu("preferences")
        imagebutton auto "gui/options_%s.png" xpos 270 ypos 30 focus_mask True action ShowMenu("preferences") hover_sound "audio/hover.mp3" activate_sound "audio/click.mp3"

        if _in_replay:

            textbutton _("End Replay") action EndReplay(confirm=True)

        elif not main_menu:

            textbutton _("Main Menu") action MainMenu()

        #textbutton _("About") action ShowMenu("about")
        imagebutton auto "gui/about_%s.png" xpos 270 ypos 50 focus_mask True action ShowMenu("about") hover_sound "audio/hover.mp3" activate_sound "audio/click.mp3"


        if renpy.variant("pc") or (renpy.variant("web") and not renpy.variant("mobile")):

            ## Help isn't necessary or relevant to mobile devices.
            #textbutton _("Help") action ShowMenu("help")
            imagebutton auto "gui/help_%s.png" xpos 270 ypos 60 focus_mask True action ShowMenu("help") hover_sound "audio/hover.mp3" activate_sound "audio/click.mp3"

        if renpy.variant("pc"):

            ## The quit button is banned on iOS and unnecessary on Android and
            ## Web.
            #textbutton _("Quit") action Quit(confirm=not main_menu)
            imagebutton auto "gui/exit_%s.png" xpos 270 ypos 70 focus_mask True action Quit(confirm=not main_menu) hover_sound "audio/hover.mp3" activate_sound "audio/click.mp3"

screen block():
    modal True
    zorder 100
    # optional: make this screen hide itself after 10.0 seconds if you forget about it
    # timer 10.0 action Hide("block")

label animation:
    show screen block
    pause 0.5
    $ persistent.main_background = False
    stop music fadeout 1
    play music "audio/flatline.mp3"fadein 1
    pause 4.5
    hide screen block

label quit:
    $ persistent.main_background = True
    return


style navigation_button is gui_button
style navigation_button_text is gui_button_text

style navigation_button:
    size_group "navigation"
    properties gui.button_properties("navigation_button")

style navigation_button_text:
    properties gui.button_text_properties("navigation_button")


## Main Menu screen ############################################################
##
## Used to display the main menu when Ren'Py starts.
##
## https://www.renpy.org/doc/html/screen_special.html#main-menu

default persistent.main_background = True
screen main_menu():

    ## This ensures that any other menu screen is replaced.
    tag menu

    if persistent.main_background:
        add gui.main_menu_background
    else:
        add "gui/4.png"
    ## This empty frame darkens the main menu.
    #frame:
    #    style "main_menu_frame"

    ## The use statement includes another screen inside this one. The actual
    ## contents of the main menu are in the navigation screen.
    use navigation

    if gui.show_name:

        vbox:
            style "main_menu_vbox"

            text "[config.name!t]":
                style "main_menu_title"

            text "[config.version]":
                style "main_menu_version"


style main_menu_frame is empty
style main_menu_vbox is vbox
style main_menu_text is gui_text
style main_menu_title is main_menu_text
style main_menu_version is main_menu_text

style main_menu_frame:
    xsize 420
    yfill True

    background "gui/overlay/main_menu.png"

style main_menu_vbox:
    xalign 1.0
    xoffset -30
    xmaximum 1200
    yalign 1.0
    yoffset -30

style main_menu_text:
    properties gui.text_properties("main_menu", accent=True)

style main_menu_title:
    properties gui.text_properties("title")

style main_menu_version:
    properties gui.text_properties("version")


## Game Menu screen ############################################################
##
## This lays out the basic common structure of a game menu screen. It's called
## with the screen title, and displays the background, title, and navigation.
##
## The scroll parameter can be None, or one of "viewport" or "vpgrid". When
## this screen is intended to be used with one or more children, which are
## transcluded (placed) inside it.

screen game_menu(title, scroll=None, yinitial=0.0):

    style_prefix "game_menu"
    if main_menu:
        add gui.main_menu_background
        add "gui/overlay/confirm.png"
        add gui.game_menu_background:
            xalign 0.5
            offset (0, 30)
    else:
        add gui.game_menu_background:
            xalign 0.5
            offset (0, 30)
    

    frame:
        style "game_menu_outer_frame"

        hbox:

            ## Reserve space for the navigation section.
            frame:
                style "game_menu_navigation_frame"

            frame:
                style "game_menu_content_frame"

                if scroll == "viewport":

                    viewport:
                        yinitial yinitial
                        scrollbars "vertical"
                        mousewheel True
                        draggable True
                        pagekeys True

                        side_yfill True

                        vbox:
                            transclude

                elif scroll == "vpgrid":

                    vpgrid:
                        cols 1
                        yinitial yinitial

                        scrollbars "vertical"
                        mousewheel True
                        draggable True
                        pagekeys True

                        side_yfill True

                        transclude

                else:

                    transclude

    use navigation_2

    imagebutton auto "gui/button/returnbutton_%s.png":
        
        style "return_button"

        action Return()

    label title

    if main_menu:
        key "game_menu" action ShowMenu("main_menu")


style game_menu_outer_frame is empty
style game_menu_navigation_frame is empty
style game_menu_content_frame is empty
style game_menu_viewport is gui_viewport
style game_menu_side is gui_side
style game_menu_scrollbar is gui_vscrollbar

style game_menu_label is gui_label
style game_menu_label_text is gui_label_text

style return_button is navigation_button
style return_button_text is navigation_button_text

style game_menu_outer_frame:
    bottom_padding 45
    top_padding 180

    #background "gui/overlay/game_menu.png"

style game_menu_navigation_frame:
    xsize 420
    yfill True

style game_menu_content_frame:
    left_margin 60
    right_margin 30
    top_margin 15

style game_menu_viewport:
    xsize 1380

style game_menu_vscrollbar:
    unscrollable gui.unscrollable

style game_menu_side:
    spacing 15

style game_menu_label:
    xpos 75
    ysize 180

style game_menu_label_text:
    size gui.title_text_size
    color gui.accent_color
    yalign 0.5

style return_button:
    xpos 130
    yalign 1.0
    yoffset -45


## About screen ################################################################
##
## This screen gives credit and copyright information about the game and Ren'Py.
##
## There's nothing special about this screen, and hence it also serves as an
## example of how to make a custom screen.

screen about():

    tag menu

    ## This use statement includes the game_menu screen inside this one. The
    ## vbox child is then included inside the viewport inside the game_menu
    ## screen.
    use game_menu(_("About"), scroll="viewport"):

        style_prefix "about"

        vbox:

            label "[config.name!t]"
            text _("Version [config.version!t]\n")

            ## gui.about is usually set in options.rpy.
            if gui.about:
                text "[gui.about!t]\n"

            text _("Made with {a=https://www.renpy.org/}Ren'Py{/a} [renpy.version_only].\n\n[renpy.license!t]")


style about_label is gui_label
style about_label_text is gui_label_text
style about_text is gui_text

style about_label_text:
    size gui.label_text_size


## Load and Save screens #######################################################
##
## These screens are responsible for letting the player save the game and load
## it again. Since they share nearly everything in common, both are implemented
## in terms of a third screen, file_slots.
##
## https://www.renpy.org/doc/html/screen_special.html#save https://
## www.renpy.org/doc/html/screen_special.html#load

screen save():
    tag menu
    use file_slots(_(""))
    add "gui/diary_save.png":
        offset(370,10)

screen load():
    tag menu
    use file_slots(_(""))
    add "gui/diary_load.png":
        offset(370,10)

screen file_slots(title):

    default page_name_value = FilePageNameInputValue(pattern=_("Page {}"), auto=_("Automatic Saves"), quick=_("Quick Saves"))

    use game_menu(title):

        fixed:

            ## This ensures the input will get the enter event before any of the
            ## buttons do.
            order_reverse True

            ## The page name, which can be edited by/hovering on a button.
            button:
                style "page_label"

                key_events True
                xalign 0.5
                offset(20,760)
                action page_name_value.Toggle()

                input:
                    style "page_label_text"
                    value page_name_value

            ## The grid of file slots.
            grid gui.file_slot_cols gui.file_slot_rows:
                style_prefix "slot"

                xalign 0.5
                yalign 0.5
                offset(-225,-60)

                spacing gui.slot_spacing

                for i in range(gui.file_slot_cols * gui.file_slot_rows):

                    $ slot = i + 1

                    button:
                        action FileAction(slot)

                        has vbox

                        add FileScreenshot(slot) xalign 0.5

                        text FileTime(slot, format=_("""
{#file_time}%A, %B %d %Y, %H:%M""")):
                            style "slot_time_text"

                        text FileSaveName(slot):
                            style "slot_name_text"

                        key "save_delete" action FileDelete(slot)

            ## Buttons to access other pages.
            hbox:
                style_prefix "page"

                xalign 0.5
                yalign 1.0
                offset(-480, -25)

                spacing gui.page_spacing

                textbutton _("<") action FilePagePrevious()

                if config.has_autosave:
                    textbutton _("{#auto_page}A") action FilePage("auto")

                if config.has_quicksave:
                    textbutton _("{#quick_page}Q") action FilePage("quick")

                ## range(1, 10) gives the numbers from 1 to 9.
                for page in range(1, 4):
                    textbutton "[page]" action FilePage(page)

                textbutton _(">") action FilePageNext()


style page_label is gui_label
style page_label_text is gui_label_text
style page_button is gui_button
style page_button_text is gui_button_text

style slot_button is gui_button
style slot_button_text is gui_button_text
style slot_time_text is slot_button_text
style slot_name_text is slot_button_text

style page_label:
    xpadding 75
    ypadding 5

style page_label_text:
    text_align 0.5
    layout "subtitle"
    hover_color gui.hover_color

style page_button:
    properties gui.button_properties("page_button")

style page_button_text:
    properties gui.button_text_properties("page_button")

style slot_button:
    properties gui.button_properties("slot_button")

style slot_button_text:
    properties gui.button_text_properties("slot_button")


## Preferences screen ##########################################################
##
## The preferences screen allows the player to configure the game to better suit
## themselves.
##
## https://www.renpy.org/doc/html/screen_special.html#preferences

screen preferences():

    tag menu

    use game_menu(_("")):
        frame:
            offset(-118, -100)
            background "gui/optionsasset.png"
            if renpy.variant("pc") or renpy.variant("web"):
                vbox:
                    offset(25,100)
                    label _("Screen Size")
                    style_prefix "radio"
                    textbutton _("Window") action Preference("display", "window")
                    textbutton _("Fullscreen") action Preference("display", "fullscreen")

                vbox:
                    style_prefix "radio"
                    offset(300,100)
                    label _("Rollback Side")
                    textbutton _("Disable") action Preference("rollback side", "disable")
                    textbutton _("Left") action Preference("rollback side", "left")
                    textbutton _("Right") action Preference("rollback side", "right")

                vbox:
                    style_prefix "check"
                    offset(640,98)
                    label _("Skip")
                    textbutton _("Unseen Text") action Preference("skip", "toggle")
                    textbutton _("After Choices") action Preference("after choices", "toggle")
                    textbutton _("Transitions") action InvertSelected(Preference("transitions", "toggle"))

                ## Additional vboxes of type "radio_pref" or "check_pref" can be
                ## added here, to add additional creator-defined preferences.

            null height (2 * gui.pref_spacing)

            hbox:
                style_prefix "slider"
                box_wrap True
                offset(-10,500)

                vbox:
                    offset((24,0))

                    label _("Text Speed")

                    bar value Preference("text speed")

                    label _("Auto-Forward Time")

                    bar value Preference("auto-forward time")

                vbox:
                    offset(-24,0)

                    if config.has_music:
                        label _("Music Volume")

                        hbox:
                            bar value Preference("music volume")

                    if config.has_sound:

                        label _("Sound Volume")

                        hbox:
                            bar value Preference("sound volume")

                            if config.sample_sound:
                                textbutton _("Test") action Play("sound", config.sample_sound)


                    if config.has_voice:
                        label _("Voice Volume")

                        hbox:
                            bar value Preference("voice volume")

                            if config.sample_voice:
                                textbutton _("Test") action Play("voice", config.sample_voice)

                    if config.has_music or config.has_sound or config.has_voice:
                        null height gui.pref_spacing

                        textbutton _("Mute All"):
                            action Preference("all mute", "toggle")
                            style "mute_all_button"


style pref_label is gui_label
style pref_label_text is gui_label_text
style pref_vbox is vbox

style radio_label is pref_label
style radio_label_text is pref_label_text
style radio_button is gui_button
style radio_button_text is gui_button_text
style radio_vbox is pref_vbox

style check_label is pref_label
style check_label_text is pref_label_text
style check_button is gui_button
style check_button_text is gui_button_text
style check_vbox is pref_vbox

style slider_label is pref_label
style slider_label_text is pref_label_text
style slider_slider is gui_slider
style slider_button is gui_button
style slider_button_text is gui_button_text
style slider_pref_vbox is pref_vbox

style mute_all_button is check_button
style mute_all_button_text is check_button_text

style pref_label:
    top_margin gui.pref_spacing
    bottom_margin 3

style pref_label_text:
    yalign 1.0

style pref_vbox:
    xsize 338

style radio_vbox:
    spacing gui.pref_button_spacing

style radio_button:
    properties gui.button_properties("radio_button")
    foreground "gui/button/radio_[prefix_]foreground.png"

style radio_button_text:
    properties gui.button_text_properties("radio_button")

style check_vbox:
    spacing gui.pref_button_spacing

style check_button:
    properties gui.button_properties("check_button")
    foreground "gui/button/check_[prefix_]foreground.png"

style check_button_text:
    properties gui.button_text_properties("check_button")

style slider_slider:
    xsize 525

style slider_button:
    properties gui.button_properties("slider_button")
    yalign 0.5
    left_margin 15

style slider_button_text:
    properties gui.button_text_properties("slider_button")

style slider_vbox:
    xsize 675


## History screen ##############################################################
##
## This is a screen that displays the dialogue history to the player. While
## there isn't anything special about this screen, it does have to access the
## dialogue history stored in _history_list.
##
## https://www.renpy.org/doc/html/history.html

screen character_sheet():

    tag menu

    default selected_character = York_Crux

    use game_menu(_(""))
    frame:
        offset(275, 35)
        background "gui/notesasset.png"
        
        hbox:
            offset(95,50)
            textbutton _("[York_Crux.name]") action SetScreenVariable("selected_character", York_Crux) text_size 25
            text _("|")
            textbutton _("[Black_Lumaban.name]") action SetScreenVariable("selected_character", Black_Lumaban) text_size 25
            text _("|")
            textbutton _("[Grete_Braun.name]") action SetScreenVariable("selected_character", Grete_Braun) text_size 25
        viewport id "vp":
            draggable True
            mousewheel True
            area(700,135,575,586)
            vbox:
                label _(selected_character.name) 
                label _("")
                label _("First Impressions:") text_size 30
                label _(selected_character.first_impression) text_size 25    
        if selected_character.image_name == "images/character_icons/questionmark.png":
            add selected_character.image_name offset(290, 290)
        else:
            add selected_character.image_name offset(80, 60)

style inventory_label:
    xalign 0.2

style slot:
    background Frame("gui/square.png",0,0)
    minimum(100,100)
    maximum(100,100)
    xalign 0.5
                
screen history():

    tag menu

    ## Avoid predicting this screen, as it can be very large.
    predict False

    use game_menu(_("")):

        frame:
            background "gui/historyasset.png"
            offset(-270,-160)

            vpgrid:
                offset(230,170)
                
                style_prefix "history"

                cols 1

                draggable True
                mousewheel True
                
                yalign 0.5
                xalign 0.5
                ymaximum 735

                xmaximum 1500

                for h in _history_list:

                    window:

                        ## This lays things out properly if history_height is None.
                        has fixed:
                            yfit True

                        if h.who:

                            label h.who:
                                style "history_name"
                                substitute False

                                ## Take the color of the who text from the Character, if
                                ## set.
                                if "color" in h.who_args:
                                    text_color h.who_args["color"]

                        $ what = renpy.filter_text_tags(h.what, allow=gui.history_allow_tags)
                        text what:
                            substitute False

                if not _history_list:
                    label _("The dialogue history is empty.") xpos 119


## This determines what tags are allowed to be displayed on the history screen.

define gui.history_allow_tags = { "alt", "noalt" }


style history_window is empty

style history_name is gui_label
style history_name_text is gui_label_text
style history_text is gui_text

style history_text is gui_text

style history_label is gui_label
style history_label_text is gui_label_text

style history_window:
    xfill True
    ysize gui.history_height

style history_name:
    xpos gui.history_name_xpos
    xanchor gui.history_name_xalign
    ypos gui.history_name_ypos
    xsize gui.history_name_width

style history_name_text:
    min_width gui.history_name_width
    text_align gui.history_name_xalign

style history_text:
    xpos gui.history_text_xpos
    ypos gui.history_text_ypos
    xanchor gui.history_text_xalign
    xsize gui.history_text_width
    min_width gui.history_text_width
    text_align gui.history_text_xalign
    layout ("subtitle" if gui.history_text_xalign else "tex")

style history_label:
    xfill True

style history_label_text:
    xalign 0.5


## Help screen #################################################################
##
## A screen that gives information about key and mouse bindings. It uses other
## screens (keyboard_help, mouse_help, and gamepad_help) to display the actual
## help.

screen help():

    tag menu

    default device = "keyboard"

    use game_menu(_("")):

        style_prefix "help"

        frame:
            background "gui/helpasset.png"
            offset(-270,-165)

            vbox:
                offset(130,167)
                spacing 23
                hbox:
                    textbutton _("Keyboard") action SetScreenVariable("device", "keyboard")
                    textbutton _("Mouse") action SetScreenVariable("device", "mouse")

                    if GamepadExists():
                        textbutton _("Gamepad") action SetScreenVariable("device", "gamepad")

                if device == "keyboard":
                    use keyboard_help
                elif device == "mouse":
                    use mouse_help
                elif device == "gamepad":
                    use gamepad_help


screen keyboard_help():
    hbox:
        offset(-190,-10)
        label _("Enter")
        text _('''Advances dialogue and 
activates the interface.''')

    hbox:
        offset(-180,-10)
        label _("Space")
        text _('''Advances dialogue 
without selecting 
choices.''')

    hbox:
        offset(-185,-20)
        label _('''Arrow
Keys''')
        text _('''Navigate the interface.''')

    hbox:
        offset(-170,-10)
        label _("Escape")
        text _('''Accesses the game 
menu.''')

    hbox:
        offset(-230,-20)
        label _("Ctrl")
        text _('''Skips dialogue while held
down.''')

    hbox:
        offset(-230,-20)
        label _("Tab")
        text _("Toggles dialogue skipping.")

    hbox:
        offset(-150,-20)
        label _("Page Up")
        text _('''Rolls back to earlier 
dialogue.''')

    hbox:
        offset(500,-720)
        label _("Page Down")
        text _('''Rolls forward to 
later dialogue.''')

    hbox:
        offset(340,-730)
        label "H"
        text _("Hides the user interface.")

    hbox:
        offset(340,-730)
        label "S"
        text _("Takes a screenshot.")

    hbox:
        offset(340,-730)
        label "V"
        text _("Toggles assistive {a=https://www.renpy.org/l/voicing}self-voicing{/a}.")

    hbox:
        offset(450,-729)
        label "Shift+A"
        text _('''Opens the accessibility 
menu.''')


screen mouse_help():

    hbox:
        offset(-150,-10)
        label _("Left/hover")
        text _('''Advances dialogue and
activates the interface.''')

    hbox:
        offset(-100,-10)
        label _("Middle/hover")
        text _('''Hides the user 
interface.''')

    hbox:
        offset(-120,-16)
        label _("Right/hover")
        text _('''Accesses the game 
menu.''')

    hbox:
        offset(-24,-17)
        label _("Mouse Wheel Up/hover Rollback Side")
        text _('''Rolls back to 
earlier dialogue.''')

    hbox:
        offset(10,-17)
        label _("Mouse Wheel Down")
        text _('''Rolls forward 
to later 
dialogue.''')


screen gamepad_help():

    hbox:
        offset(-35,-8)
        label _("Right Trigger\nA/Bottom Button")
        text _("Advances\ndialogue and\nactivates the\ninterface.")

    hbox:
        offset(-80,-8)
        label _("Left Trigger\nLeft Shoulder")
        text _('''Rolls back to 
earlier dialogue.''')

    hbox:
        offset(-50,-8)
        label _("Right Shoulder")
        text _('''Rolls forward to 
later dialogue.''')


    hbox:
        offset(-80,-8)
        label _("D-Pad, Sticks")
        text _('''Navigate the 
interface.''')

    hbox:
        offset(-80,-8)
        label _("Start, Guide")
        text _('''Accesses the game
menu.''')

    hbox:
        offset(-80,-8)
        label _("Y/Top Button")
        text _('''Hides the user 
interface.''')

    textbutton _("Calibrate") action GamepadCalibrate() offset(40,-20)


style help_button is gui_button
style help_button_text is gui_button_text
style help_label is gui_label
style help_label_text is gui_label_text
style help_text is gui_text

style help_button:
    properties gui.button_properties("help_button")
    xmargin 12

style help_button_text:
    properties gui.button_text_properties("help_button")

style help_label:
    xsize 375
    right_padding 30

style help_label_text:
    size gui.text_size
    xalign 1.0
    text_align 1.0



################################################################################
## Additional screens
################################################################################


## Confirm screen ##############################################################
##
## The confirm screen is called when Ren'Py wants to ask the player a yes or no
## question.
##
## https://www.renpy.org/doc/html/screen_special.html#confirm

screen confirm(message, yes_action, no_action):

    ## Ensure other screens do not get input while this screen is displayed.
    modal True

    zorder 200

    style_prefix "confirm"

    add "gui/overlay/confirm.png"


    vbox:
        xalign .5
        yalign .5
        spacing 0
        frame:
            background Frame("gui/ticket.png", 754,400,0,0) pos(0.85,0.8)
            if message == layout.QUIT:
                add "gui/quit.png":
                    xalign 0.5
                    offset (-695, 65)

            elif message == layout.MAIN_MENU:
                add "gui/mainmenu.png":
                    xalign 0.5
                    offset (-695, 75)
            
            elif message == layout.LOADING:
                add "gui/loading.png":
                    xalign 0.5
                    offset (-695, 65)
            
            elif message == layout.OVERWRITE_SAVE:
                add "gui/overwritesave.png":
                    xalign 0.5
                    offset (-695, 70)
            
            elif message == layout.ARE_YOU_SURE:
                add "gui/areyousure.png":
                    xalign 0.5
                    offset (-695, 65)

            elif message == layout.DELETE_SAVE:
                add "gui/deletesave.png":
                    xalign 0.5
                    offset (-692.5, 65)

            else:
                text _(message):
                    xalign 0.5
                    offset (-50, -16)

            hbox:
                xalign 0.4
                spacing 160

                imagebutton auto "gui/yesv_%s.png":
                    action yes_action
                    offset (-515, 180)
                imagebutton auto "gui/nov_%s.png":
                    action no_action
                    offset (-595, 180)

    ## Right/hover and escape answer "no".
    key "game_menu" action no_action


style confirm_frame is gui_frame
style confirm_prompt is gui_prompt
style confirm_prompt_text is gui_prompt_text
style confirm_button is gui_medium_button
style confirm_button_text is gui_medium_button_text

style confirm_frame:
    background Frame([ "gui/confirm_frame.png", "gui/frame.png"], gui.confirm_frame_borders, tile=gui.frame_tile)
    padding gui.confirm_frame_borders.padding
    xalign .5
    yalign .5

style confirm_prompt_text:
    text_align 0.5
    layout "subtitle"

style confirm_button:
    properties gui.button_properties("confirm_button")

style confirm_button_text:
    properties gui.button_text_properties("confirm_button")


## Skip indicator screen #######################################################
##
## The skip_indicator screen is displayed to indicate that skipping is in
## progress.
##
## https://www.renpy.org/doc/html/screen_special.html#skip-indicator

screen skip_indicator():

    zorder 100
    style_prefix "skip"

    frame:

        hbox:
            spacing 9

            text _("Skipping")

            text "▸" at delayed_blink(0.0, 1.0) style "skip_triangle"
            text "▸" at delayed_blink(0.2, 1.0) style "skip_triangle"
            text "▸" at delayed_blink(0.4, 1.0) style "skip_triangle"


## This transform is used to blink the arrows one after another.
transform delayed_blink(delay, cycle):
    alpha .5

    pause delay

    block:
        linear .2 alpha 1.0
        pause .2
        linear .2 alpha 0.5
        pause (cycle - .4)
        repeat


style skip_frame is empty
style skip_text is gui_text
style skip_triangle is skip_text

style skip_frame:
    ypos gui.skip_ypos
    background Frame("gui/skip.png", gui.skip_frame_borders, tile=gui.frame_tile)
    padding gui.skip_frame_borders.padding

style skip_text:
    size gui.notify_text_size

style skip_triangle:
    ## We have to use a font that has the BLACK RIGHT-POINTING SMALL TRIANGLE
    ## glyph in it.
    font "DejaVuSans.ttf"


## Notify screen ###############################################################
##
## The notify screen is used to show the player a message. (For example, when
## the game is quicksaved or a screenshot has been taken.)
##
## https://www.renpy.org/doc/html/screen_special.html#notify-screen

screen notify(message):

    zorder 100
    style_prefix "notify"

    frame at notify_appear:
        text "[message!tq]"

    timer 3.25 action Hide('notify')


transform notify_appear:
    on show:
        alpha 0
        linear .25 alpha 1.0
    on hide:
        linear .5 alpha 0.0


style notify_frame is empty
style notify_text is gui_text

style notify_frame:
    ypos gui.notify_ypos

    background Frame("gui/notify.png", gui.notify_frame_borders, tile=gui.frame_tile)
    padding gui.notify_frame_borders.padding

style notify_text:
    properties gui.text_properties("notify")


## NVL screen ##################################################################
##
## This screen is used for NVL-mode dialogue and menus.
##
## https://www.renpy.org/doc/html/screen_special.html#nvl


screen nvl(dialogue, items=None):

    window:
        style "nvl_window"

        has vbox:
            spacing gui.nvl_spacing

        ## Displays dialogue in either a vpgrid or the vbox.
        if gui.nvl_height:

            vpgrid:
                cols 1
                yinitial 1.0

                use nvl_dialogue(dialogue)

        else:

            use nvl_dialogue(dialogue)

        ## Displays the menu, if given. The menu may be displayed incorrectly if
        ## config.narrator_menu is set to True, as it is above.
        for i in items:

            textbutton i.caption:
                action i.action
                style "nvl_button"

    add SideImage() xalign 0.0 yalign 1.0


screen nvl_dialogue(dialogue):

    for d in dialogue:

        window:
            id d.window_id

            fixed:
                yfit gui.nvl_height is None

                if d.who is not None:

                    text d.who:
                        id d.who_id

                text d.what:
                    id d.what_id


## This controls the maximum number of NVL-mode entries that can be displayed at
## once.
define config.nvl_list_length = gui.nvl_list_length

style nvl_window is default
style nvl_entry is default

style nvl_label is say_label
style nvl_dialogue is say_dialogue

style nvl_button is button
style nvl_button_text is button_text

style nvl_window:
    xfill True
    yfill True

    background "gui/nvl.png"
    padding gui.nvl_borders.padding

style nvl_entry:
    xfill True
    ysize gui.nvl_height

style nvl_label:
    xpos gui.nvl_name_xpos
    xanchor gui.nvl_name_xalign
    ypos gui.nvl_name_ypos
    yanchor 0.0
    xsize gui.nvl_name_width
    min_width gui.nvl_name_width
    text_align gui.nvl_name_xalign

style nvl_dialogue:
    xpos gui.nvl_text_xpos
    xanchor gui.nvl_text_xalign
    ypos gui.nvl_text_ypos
    xsize gui.nvl_text_width
    min_width gui.nvl_text_width
    text_align gui.nvl_text_xalign
    layout ("subtitle" if gui.nvl_text_xalign else "tex")

style nvl_thought:
    xpos gui.nvl_thought_xpos
    xanchor gui.nvl_thought_xalign
    ypos gui.nvl_thought_ypos
    xsize gui.nvl_thought_width
    min_width gui.nvl_thought_width
    text_align gui.nvl_thought_xalign
    layout ("subtitle" if gui.nvl_text_xalign else "tex")

style nvl_button:
    properties gui.button_properties("nvl_button")
    xpos gui.nvl_button_xpos
    xanchor gui.nvl_button_xalign

style nvl_button_text:
    properties gui.button_text_properties("nvl_button")



################################################################################
## Mobile Variants
################################################################################

style pref_vbox:
    variant "medium"
    xsize 675

## Since a mouse may not be present, we replace the quick menu with a version
## that uses fewer and bigger buttons that are easier to touch.
screen quick_menu():
    variant "touch"

    zorder 100

    if quick_menu:

        hbox:
            style_prefix "quick"

            xalign 0.5
            yalign 1.0

            textbutton _("Back") action Rollback()
            textbutton _("Skip") action Skip() alternate Skip(fast=True, confirm=True)
            textbutton _("Auto") action Preference("auto-forward", "toggle")
            textbutton _("Menu") action ShowMenu()


style window:
    variant "small"
    background "gui/phone/textbox.png"

style radio_button:
    variant "small"
    foreground "gui/phone/button/radio_[prefix_]foreground.png"

style check_button:
    variant "small"
    foreground "gui/phone/button/check_[prefix_]foreground.png"

style nvl_window:
    variant "small"
    background "gui/phone/nvl.png"

style main_menu_frame:
    variant "small"
    background "gui/phone/overlay/main_menu.png"

style game_menu_outer_frame:
    variant "small"
    background "gui/phone/overlay/game_menu.png"

style game_menu_navigation_frame:
    variant "small"
    xsize 510

style game_menu_content_frame:
    variant "small"
    top_margin 0

style pref_vbox:
    variant "small"
    xsize 600

style bar:
    variant "small"
    ysize gui.bar_size
    left_bar Frame("gui/phone/bar/left.png", gui.bar_borders, tile=gui.bar_tile)
    right_bar Frame("gui/phone/bar/right.png", gui.bar_borders, tile=gui.bar_tile)

style vbar:
    variant "small"
    xsize gui.bar_size
    top_bar Frame("gui/phone/bar/top.png", gui.vbar_borders, tile=gui.bar_tile)
    bottom_bar Frame("gui/phone/bar/bottom.png", gui.vbar_borders, tile=gui.bar_tile)

style scrollbar:
    variant "small"
    ysize gui.scrollbar_size
    base_bar Frame("gui/phone/scrollbar/horizontal_[prefix_]bar.png", gui.scrollbar_borders, tile=gui.scrollbar_tile)
    thumb Frame("gui/phone/scrollbar/horizontal_[prefix_]thumb.png", gui.scrollbar_borders, tile=gui.scrollbar_tile)

style vscrollbar:
    variant "small"
    xsize gui.scrollbar_size
    base_bar Frame("gui/phone/scrollbar/vertical_[prefix_]bar.png", gui.vscrollbar_borders, tile=gui.scrollbar_tile)
    thumb Frame("gui/phone/scrollbar/vertical_[prefix_]thumb.png", gui.vscrollbar_borders, tile=gui.scrollbar_tile)

style slider:
    variant "small"
    ysize gui.slider_size
    base_bar Frame("gui/phone/slider/horizontal_[prefix_]bar.png", gui.slider_borders, tile=gui.slider_tile)
    thumb "gui/phone/slider/horizontal_[prefix_]thumb.png"

style vslider:
    variant "small"
    xsize gui.slider_size
    base_bar Frame("gui/phone/slider/vertical_[prefix_]bar.png", gui.vslider_borders, tile=gui.slider_tile)
    thumb "gui/phone/slider/vertical_[prefix_]thumb.png"

style slider_vbox:
    variant "small"
    xsize None

style slider_slider:
    variant "small"
    xsize 900
