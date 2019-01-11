import maya.cmds as cmds
import math as ma
import random as rand
from functools import partial

#TODO: after building is built, create roof.
#TODO: redesign the UI = fixed
#TODO: make it so multisided building can have more than 1 side = fixed
#TODO: texture functionality = maybe later
#TODO: fix step warning = fixed
#TODO: fix list index out of range error = fixed
#TODO: if no building side is supplied then use default one. = fixed
#TODO: if obj in a group error out
#TODO: why 7 not work for multiSide=fixed
#TODO: delete old groups = fixed
#TODO: Remove item from any groups = Fixed
#TODO: fix namespace issue
#TODO: maybe error out if object with same name exists

#user will select a wall they have created and it will create a building

class BuildingCreator():
    def __init__(self):
        pass

    #get the size of walls
    def getSizes(self, object, *args):

        shapes = cmds.listRelatives(object, shapes=True)
        objSize = cmds.listRelatives(object, parent=True)

        #get the bounding box of the shape
        sizeMinX = cmds.getAttr(shapes[0] + '.boundingBoxMinX')
        sizeMaxX = cmds.getAttr(shapes[0] + '.boundingBoxMaxX')
        sizeMinY = cmds.getAttr(shapes[0] + '.boundingBoxMinY')
        sizeMaxY = cmds.getAttr(shapes[0] + '.boundingBoxMaxY')
        sizeMinZ = cmds.getAttr(shapes[0] + '.boundingBoxMinZ')
        sizeMaxZ = cmds.getAttr(shapes[0] + '.boundingBoxMaxZ')

        #get the scale to add to the bounding box
        scaleX = cmds.getAttr(objSize[0] + '.scaleX')
        scaleY = cmds.getAttr(objSize[0] + '.scaleY')
        scaleZ = cmds.getAttr(objSize[0] + '.scaleZ')

        print sizeMaxX
        print sizeMinX
        print scaleX
        print scaleY
        print scaleZ

        #get the sizes
        if sizeMinX<0 and sizeMaxX<0:
            self.sizeX = abs(abs(sizeMinX) - abs(sizeMaxX)) * abs(scaleX)
        elif sizeMinX>0 and sizeMaxX>0:
            self.sizeX = abs(abs(sizeMinX) - abs(sizeMaxX)) * abs(scaleX)
        else:
            self.sizeX = abs(abs(sizeMinX) + abs(sizeMaxX)) * abs(scaleX)

        if sizeMinY<0 and sizeMaxY<0:
            self.sizeY = abs(abs(sizeMinY) - abs(sizeMaxY)) * abs(scaleY)
        elif sizeMinY>0 and sizeMaxY>0:
            self.sizeY = abs(abs(sizeMinY) - abs(sizeMaxY)) * abs(scaleY)
        else:
            self.sizeY = abs(abs(sizeMinY) + abs(sizeMaxY)) * abs(scaleY)

        if sizeMinZ<0 and sizeMaxZ<0:
            self.sizeZ = abs(abs(sizeMinZ) - abs(sizeMaxZ)) * abs(scaleZ)
        elif sizeMinZ>0 and sizeMaxZ>0:
            self.sizeZ = abs(abs(sizeMinZ) - abs(sizeMaxZ)) * abs(scaleZ)
        else:
            self.sizeZ = abs(abs(sizeMinZ) + abs(sizeMaxZ)) * abs(scaleZ)

        sizeList = [self.sizeX, self.sizeY, self.sizeZ]

        return sizeList


    #for creating rectangular buildings
    def squareBuilding(self, name, buildingName, width, length, height):

        wallSection = cmds.ls(sl=True, dag=True)
        print wallSection

        if (len(wallSection) <= 0):
            buildingWall = self.defaultBuilding()
            cmds.select('Wall')
            self.squareWall = cmds.ls(sl=True,dag=True)
        else:
            self.squareWall = cmds.ls(sl=True,dag=True)


        squareBuildingSizeList = self.getSizes(self.squareWall)
        self.name = cmds.rename(self.squareWall[0], name,ignoreShape=True)

        objWidth = squareBuildingSizeList[0]
        objHeight = squareBuildingSizeList[1]
        objLength = squareBuildingSizeList[2]

        xPivot = (objWidth/2)
        yPivot = (objHeight/2)
        zPivot = (objLength/2)

        #set centerPivot to the object and freeze transforms
        cmds.xform(self.name, cp = True)
        cmds.makeIdentity(apply=True, t=1, r=1, s=1, n=0)
        cmds.move(xPivot, -(yPivot), zPivot, self.name + '.scalePivot', self.name + '.rotatePivot', os = True, relative = True)

        buildingWalls = []
        #move the pivot point of the object
        #first Axis
        bWidth = 1
        while bWidth <= width:
            self.bWallL1 = cmds.duplicate(rc=True)
            cmds.move(-objWidth,0,0,ls=True,r=True)
            bWidth += 1
            buildingWalls.append(self.bWallL1)
        cmds.rotate(0, -90, 0)

        bLength = 1
        while bLength <= length:
            self.bWallW1 = cmds.duplicate(rc=True)
            cmds.move(0,0,-objWidth, ls=True,r=True)
            bLength += 1
            buildingWalls.append(self.bWallW1)
        cmds.rotate(0, 180, 0)

        bWidth = 1
        while bWidth <= width:
            cmds.duplicate(rc=True)
            cmds.move(objWidth,0,0,ls=True,r=True)
            bWidth += 1
            buildingWalls.append()
        cmds.rotate(0, 90, 0)

        bLength = 1
        while bLength < length:
            cmds.duplicate(rc=True)
            cmds.move(0,0,objWidth,ls=True, r=True)
            buildingWalls.append()
            bLength += 1


        cmds.group('%s*'% self.name, n='%s*'% self.name +'_'+ 'Floors_',a=True)

        bHeight = 0
        while bHeight < (height-1):
            cmds.duplicate(rc=True)
            cmds.move(0,objHeight,0,ls=True,r=True)
            bHeight += 1

        cmds.group('%s*'% self.name +'_'+ buildingName +'_'+'Floors_*', n='%s' %buildingName + '_Building_',a=True)
        cmds.select(clear=True)


    def multiBuilding(self, name, bname, sides, width, height, *args):

        mWall = cmds.ls(sl=True, dag=True)
        self.walls = mWall[]
        if (len(self.mWall)<=0):
            buildingWall = self.defaultBuilding()
            cmds.select('Wall')
            self.mWall = cmds.ls(sl=True,dag=True)

        self.name = cmds.rename(self.mWall[0], name, ignoreShape=True)
        mList = self.getSizes()

        objLength = mList[0]
        objHeight = mList[1]
        objWidth = mList[2]

        sides1 = objLength * width
        print objLength
        print sides1
        print self.name

        cmds.xform(self.name, cp=True)
        cmds.makeIdentity(apply=True, t=1, r=1, s=1, n=0)
        apotheom = sides1/(2*(ma.tan(ma.pi/sides)))
        apothTrue = apotheom - abs(objWidth/2)

        print apotheom
        print apothTrue

        NumSides = 1
        while NumSides < width:
            cmds.duplicate(rc=True)
            cmds.move(-objLength, 0, 0, ls=True, r=True)
            NumSides += 1
        self.bSide = cmds.group(name + '*', n='wall')

        cmds.xform(self.bSide, cp=True)
        cmds.move(0,0,-apothTrue, self.bSide + '.scalePivot', self.bSide + '.rotatePivot', ws = True, relative = True)

        angles = float(float(360)/float(sides))
        print angles

        for i in range(sides-1):
            cmds.duplicate(rc=True)
            cmds.rotate(0,angles,0,ws = True, relative = True)

        cmds.group(a=True)

        bHeight = 0
        while bHeight < (height - 1):
            cmds.duplicate(rc=True)
            cmds.move(0, objHeight, 0, ls=True, r=True)
            bHeight += 1

        cmds.group('%s' %self.name, n='%s' %bname, a=True)
        cmds.xform('%s*'% bname, cp=True)
        cmds.move(0,0,0,rpr=True)

        self.deleteOldGroups()

    def defaultBuilding(self):
        defaultSide = cmds.polyPlane(name='default_wall', w=2,h=3,sx=3,sy=1)
        cmds.rotate(90,0,0)
        cmds.makeIdentity(apply=True, t=1, r=1, s=1, n=0)
        cmds.select('default_wall' + '.e[3]')
        cmds.move(-0.4,0,0,r=True)
        cmds.select('default_wall' + '.e[5]')
        cmds.move(0.4,0,0,relative=True)
        cmds.select('default_wall' + '.f[2]','default_wall' + '.e[0]')
        cmds.polyExtrudeFacet(keepFacesTogether = True,thickness=0.04)
        cmds.select('default_wall' + '.f[1]')
        cmds.polyExtrudeFacet(offset=0.2)
        cmds.polySubdivideFacet('default_wall' + '.f[1]', duv = 1)
        cmds.select('default_wall' + '.f[1]','default_wall' + '.f[15:17]')
        cmds.polyExtrudeFacet(keepFacesTogether=False, offset = .02)
        cmds.select('default_wall' + '.f[18:33]')
        cmds.polyExtrudeFacet(keepFacesTogether=True,thickness=.02)
        cmds.select('default_wall' + '.f[3]','default_wall' + '.f[7:9]','default_wall' + '.f[5:6]')
        cmds.delete()
        cmds.rename('default_wall', 'Wall')

    def deleteOldGroups(self):
        tranList = cmds.ls(type = 'transform')
        for t in tranList:
            rel = cmds.listRelatives(t, c=True)
            if rel == None:
                cmds.delete(t)

    def ungroupObj(self,object):

        objParent = bool(cmds.listRelatives(object, allParents=True))
        if objParent == True:
            cmds.parent(object, world=True)



class BuildCreatorUI():

    def __init__(self):
        self.name = 'BuildingCreator'
        self.size = (500,400)
        self.Building = None

    def bWindowMain(self):

        self.close()

        bWindow = cmds.window(self.name, title = 'Building Creator', widthHeight = self.size, menuBar=True,sizeable=False)

        #Menu Items
        self.editMenu = cmds.menu('editMenu', label='Edit')
        cmds.menuItem(label="Save Settings", parent=self.editMenu)
        cmds.menuItem(label="Reset Settings", parent=self.editMenu)

        self.helpMenu = cmds.menu('helpMenu', label='Help')
        cmds.menuItem(label="Help on Tool", parent=self.helpMenu)

        self.mainForm = cmds.formLayout('mainForm')
        self.scrollLayout = cmds.scrollLayout('mainScroll',hst = 16,vst = 16,borderVisible=True)

        # Buttons
        self.rowBtn = cmds.rowLayout(numberOfColumns=2, parent=self.mainForm)
        createBtn = cmds.button(label="Create", width = 250, command=self.create, parent=self.rowBtn)
        closeBtn = cmds.button(label="Close", width=250, command=('cmds.deleteUI(\"' + bWindow + '\", window=True)'),
                               parent=self.rowBtn)

        cmds.formLayout(self.mainForm, edit = True, attachForm = [(self.scrollLayout,'left',0),
                                                                    (self.scrollLayout, 'top', 0),
                                                                    (self.scrollLayout, 'right', 0),
                                                                    (self.scrollLayout, 'bottom', 30),
                                                                  (self.rowBtn, 'bottom',0),
                                                                  (self.rowBtn, 'left', 2)])

        self.secondForm = cmds.formLayout('secondMain',parent=self.scrollLayout)
        self.nameField = cmds.textFieldGrp(label='Section Name',parent=self.secondForm)

        self.mainFrame = cmds.frameLayout(label='Buildings',collapsable=True,w=500,borderVisible=False)

        cmds.formLayout(self.secondForm, edit = True, attachForm = [(self.nameField, 'top',0),
                                                             (self.nameField,'left',0),
                                                             (self.mainFrame, 'top', 30),
                                                             (self.mainFrame, 'left', 1),
                                                             (self.mainFrame, 'bottom', 30),
                                                             (self.mainFrame, 'right', 0)])

        radioCont = cmds.radioCollection()
        self.radioLayout = cmds.formLayout('radioLayout')

        self.buildingNameRect = cmds.textFieldGrp(label='Building Name', parent=self.radioLayout)
        self.squareRadio = cmds.radioButton(label='Rectangular',parent = self.radioLayout)
        self.multiRadio = cmds.radioButton(label='Multi-Sided',parent = self.radioLayout)

        #Menu for SquareButton
        self.squareField = cmds.columnLayout(adjustableColumn=True,visible=False,parent = self.radioLayout)
        self.sWidth = cmds.intSliderGrp( field=True, label='Width' ,minValue = 1,maxValue=10,fieldMinValue=1,fieldMaxValue=10,step=1,value = 1,parent = self.squareField)
        self.sLength = cmds.intSliderGrp(field=True, label='Length', minValue=1, maxValue=10, fieldMinValue=1,
                                        fieldMaxValue=10, step=1, value =1,parent=self.squareField)
        self.sHeight = cmds.intSliderGrp(field=True, label='Height', minValue=1, maxValue=10, fieldMinValue=1,
                                        fieldMaxValue=10, step=1, value = 1, parent=self.squareField)
        cmds.radioButton(self.squareRadio, e=True, cc=partial(self.changeVis,self.squareField))

        # Menu for MultiSide
        self.multiField = cmds.columnLayout(adjustableColumn=True, visible=False, parent=self.radioLayout)
        self.mSides = cmds.intSliderGrp(field=True, label='Number of Sides', minValue=3, maxValue=10, fieldMinValue=3,
                                        fieldMaxValue=10, step=1, value = 3, parent=self.multiField)
        self.mLenSides = cmds.intSliderGrp(field=True, label='Length of Sides', minValue=1, maxValue=10, fieldMinValue=1,
                                        fieldMaxValue=10, step=1, value= 1, parent=self.multiField)
        self.mHeight = cmds.intSliderGrp(field=True, label='Height', minValue=1, maxValue=10, fieldMinValue=1,
                                         fieldMaxValue=10, step=1, value = 1, parent=self.multiField)
        cmds.radioButton(self.multiRadio, e=True, cc=partial(self.changeVis, self.multiField))
        cmds.formLayout(self.radioLayout, edit=True, attachForm=((self.buildingNameRect, 'top', 5),
                                                                 (self.buildingNameRect, 'left', 5),
                                                                 (self.squareRadio, 'left', 130),
                                                                 (self.squareRadio, 'top', 30),
                                                                 (self.multiRadio, 'left', 280),
                                                                 (self.multiRadio, 'top', 30),
                                                                 (self.squareField,'top',50),
                                                                 (self.multiField, 'top', 50),
                                                                 ))

        cmds.showWindow(bWindow)


    def changeVis(self,widget,*args):
        currentState = cmds.columnLayout(widget,q=True,visible=True)
        cmds.columnLayout(widget,e=True,visible=(1-currentState))

    def create(self, *args):

        self.Building = BuildingMaker()

        sectionName = cmds.textFieldGrp(self.nameField,q=True,text=True)
        groupName = cmds.textFieldGrp(self.buildingNameRect, q=True, text=True)

        sR = cmds.radioButton(self.squareRadio, q = True, select = True)
        mR = cmds.radioButton(self.multiRadio, q = True, select = True)

        widthS = cmds.intSliderGrp(self.sWidth, q = True, value = True)
        lengthS = cmds.intSliderGrp(self.sLength, q = True, value = True)
        heightS = cmds.intSliderGrp(self.sHeight, q = True, value = True)

        sidesM = cmds.intSliderGrp(self.mSides, q=True, value=True)
        sideLengthM  = cmds.intSliderGrp(self.mLenSides,q=True,value=True)
        heightM = cmds.intSliderGrp(self.mHeight, q=True, value=True)

        if sR:
            self.Building.squareBuilding(sectionName,groupName,widthS,lengthS,heightS)

        if mR:
            self.Building.multiBuilding(sectionName,groupName,sidesM,sideLengthM, heightM)

    def close(self):

        if cmds.window(self.name, q = True, exists = True):
            cmds.deleteUI(self.name)



bCreator = BuildCreatorUI()
bCreator.bWindowMain()



