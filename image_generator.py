import os
import re
import logging
from PIL import Image, ImageDraw, ImageFont
import textwrap

logger = logging.getLogger(__name__)

WHITE = (253, 254, 255)
PURPLE = (147, 112, 219)
BRACKET_X_PADDING = 150
JSON_X_PADDING = 215
FONT_SIZE = 40
TERM_PROPERTY = 'term'
DEFINITION_PROPERTY = 'definition'
EDITOR_IMAGE_PATH = 'assets/editor_purple.png'


def get_text_dimensions(text_string, font):
    descent = font.getmetrics()[1]
    text_width = font.getmask(text_string).getbbox()[2]
    text_height = font.getmask(text_string).getbbox()[3] + descent
    return (text_width, text_height)


def create_tweet_image(tweet_term, tweet_definition):
    logger.info("Creating tweet image...")
    term = '\": \"' + tweet_term + '\",'
    definition = '\"definition\": \"' + tweet_definition + '\"'
    try:
        # open the image and convert it to RGBA
        with Image.open(EDITOR_IMAGE_PATH) as editor_image:
            editor_image = editor_image.convert("RGBA")
            
            # create an editable version of the canvas
            image_editable = ImageDraw.Draw(editor_image)

            # wrap text to fit in the canvas
            wrapper = textwrap.TextWrapper(width=64)
            definition = wrapper.fill(text=definition)
    
            # set the font and calculate text dimensions
            font_style = ImageFont.truetype('fonts/SourceCodePro-SemiBold.ttf', FONT_SIZE)
            line_height = get_text_dimensions(term, font_style)[1]
            char_width = get_text_dimensions(term[0], font_style)[0]
            term_property_width = get_text_dimensions(TERM_PROPERTY, font_style)[0]
            definition_lines = definition.split('\n')
            definition_line_count = definition.count('\n') + 1
            definition_height = definition_line_count * line_height

            #calculate the available y padding for top and bottom of the text
            total_text_height = line_height * (definition_line_count + 3) # line_height * (definition_lines + bracket + term  + bracket)
            y_padding = round((editor_image.height - total_text_height) / 2)

            # TODO: calculate the available x padding for left and right of the text

            # calculate the x position of the text
            bracket_xpos = BRACKET_X_PADDING
            term_open_quote_xpos = JSON_X_PADDING
            term_property_xpos = term_open_quote_xpos + char_width
            term_val_xpos = term_property_xpos + term_property_width
            definition_xpos = JSON_X_PADDING
            definition_property_xpos = definition_xpos + char_width
            definition_val_first_line_xpos = definition_property_xpos + (char_width * 12)

            # calculate the y position of the text
            opening_bracket_ypos = y_padding + line_height
            term_ypos = opening_bracket_ypos + line_height
            definition_ypos = term_ypos + line_height
            closing_bracket_ypos = definition_ypos + definition_height

            # draw the opening bracket 
            image_editable.text((bracket_xpos, opening_bracket_ypos), '{', font=font_style, fill=WHITE)

            # draw the open quote around term
            image_editable.text((term_open_quote_xpos, term_ypos), '"', font=font_style, fill=WHITE)

            #draw the term property in purple
            image_editable.text((term_property_xpos, term_ypos), TERM_PROPERTY, font=font_style, fill=PURPLE)

            #draw the term name in white
            image_editable.text((term_val_xpos, term_ypos), term, font=font_style, fill=WHITE)

            #draw the open quote around the definition
            image_editable.text((definition_xpos, definition_ypos), '"', font=font_style, fill=WHITE)

            #draw the definition property in purple
            image_editable.text((definition_property_xpos, definition_ypos), DEFINITION_PROPERTY, font=font_style, fill=PURPLE)

            #draw the first line of the definition in white
            image_editable.text((definition_val_first_line_xpos, definition_ypos), definition_lines[0][11:], font=font_style, fill=WHITE)

            #draw the rest of the definition in white using a loop to dynamically set the y position
            i = 1
            for line in definition_lines[1:]:
                image_editable.text((definition_xpos, definition_ypos + (line_height * i)), line, font=font_style, fill=WHITE)
                i += 1

            #draw the closing bracket
            image_editable.text((bracket_xpos, closing_bracket_ypos), '}', font=font_style, fill=WHITE)

            # normalize the path to remove any invalid characters
            image_path = re.sub(r'[\\/*?:"<>|]', '', tweet_term)

            # save the image
            editor_image.save(f"tweets/{image_path}.png", format="PNG")
            logger.info("Tweet image created...")
            return image_path
    except Exception as err:
        logger.error("Error creating tweet image...", exc_info=True)
        raise