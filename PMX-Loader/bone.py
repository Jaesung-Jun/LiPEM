from OpenGL.GL import *
import pymeshio

def main_bone_info():    
    #머리
    HEAD = "首"

    #왼팔
    LEFT_ARM = "左腕"
    #왼팔목
    LEFT_ELBOW = "左ひじ"
    #왼손목
    LEFT_WRIST = "左手首"
    
    #오른팔
    RIGHT_ARM = "右腕"
    #오른팔목
    RIGHT_ELBOW = "右ひじ"
    #오른손목
    RIGHT_WRIST = "右手首"

    #왼발
    LEFT_FOOT = "左足"
    LEFT_KNEE = "左ひざ"
    LEFT_ANKLE = "左足首"

    #오른발
    RIGHT_FOOT = "右足"
    RIGHT_KNEE = "右ひざ"
    RIGHT_ANKLE = "右足首"
    WAIST = "腰"

    main_bone = [HEAD, LEFT_ARM, LEFT_ELBOW, LEFT_WRIST, 
                RIGHT_ARM, RIGHT_ELBOW, RIGHT_WRIST, 
                LEFT_FOOT, LEFT_KNEE, LEFT_ANKLE, 
                RIGHT_FOOT, RIGHT_KNEE, RIGHT_ANKLE, WAIST]
    return main_bone