# basic imports
import maya.OpenMaya as om
import maya.cmds as cmds
import os
from functools import partial
import maya.mel as mel


def imageSize(imagePath):
    image = om.MImage()
    image.readFromFile(imagePath)

    util = om.MScriptUtil()
    widthUtil = om.MScriptUtil()
    heightUtil = om.MScriptUtil()

    widthPtr = widthUtil.asUintPtr()
    heightPtr = heightUtil.asUintPtr()

    image.getSize(widthPtr, heightPtr)
    width = widthUtil.getUint(widthPtr)
    height = heightUtil.getUint(heightPtr)

    return width, height


def createPlaneT(tPlane, *args):

    topDown = imageSize(tPlane)
    widthTop = topDown[0]
    heightTop = topDown[1]

    if cmds.objExists('topView'):
        cmds.select('topView')
        cmds.delete()
        topPlane = cmds.polyPlane(name='topView', width=float(widthTop / 10), height=float(heightTop / 10), sx=0,
                                  sy=0)
    else:
        topPlane = cmds.polyPlane(name='topView', width=float(widthTop / 10), height=float(heightTop / 10), sx=0,
                                  sy=0)
    cmds.rotate(0, 180, 0, topPlane)
    cmds.move(0, -((heightTop / 10) / 2), 0, ws=True, r=True)

def createPlaneS(sPlane, *args):

    side = imageSize(sPlane)
    widthSide = side[0]
    heightSide = side[1]

    if cmds.objExists('sideView'):
        cmds.select('sideView')
        cmds.delete()
        sidePlane = cmds.polyPlane(name='sideView', width=float(widthSide / 10), height=float(heightSide / 10),
                                   sx=0,
                                   sy=0)
    else:
        sidePlane = cmds.polyPlane(name='sideView', width=float(widthSide / 10), height=float(heightSide / 10),
                                   sx=0,
                                   sy=0)
    cmds.rotate(90.0, 180.0, 0.0, sidePlane)
    cmds.move(0, 0, ((heightSide/ 10) / 2), r=True)

def createPlaneF(fPlane, *args):

    front = imageSize(fPlane)
    widthFront = front[0]
    heightFront = front[1]

    if cmds.objExists('frontView'):
        cmds.select('frontView')
        cmds.delete()
        frontPlane = cmds.polyPlane(name='frontView', width=float(widthFront / 10), height=float(heightFront / 10),
                                    sx=0, sy=0)
    else:
        frontPlane = cmds.polyPlane(name='frontView', width=float(widthFront / 10), height=float(heightFront / 10),
                                    sx=0, sy=0)
    cmds.rotate(0.0, 90.0, -90.0, frontPlane)
    cmds.move(-((widthFront / 10) / 2), 0, 0, r=True)



def applyTex(iPathT, iPathS, iPathF):
    # TODO: make Material
    # TODO: connect image file to material
    # TODO: connect material to object
    # TODO: make sure the uvs are all correct

    mel.eval('hyperShadePanelMenuCommand("hyperShadePanel", "deleteUnusedNodes");')

    if iPathT is not None:
        shaderT = cmds.shadingNode('lambert', name='topShader', asShader=True)
        file_nodeT = cmds.shadingNode("file", name='tTex', asTexture=True)
        cmds.setAttr(file_nodeT + '.fileTextureName', iPathT, type='string')
        shading_group1 = cmds.sets(renderable=True, noSurfaceShader=True, empty=True)

        # connect shader to sg surface shader
        cmds.connectAttr('%s.outColor' % shaderT, '%s.surfaceShader' % shading_group1)
        # connect file texture node to shader's color
        cmds.connectAttr('%s.outColor' % file_nodeT, '%s.color' % shaderT)

        createPlaneT(iPathT)

        cmds.select('topView')
        cmds.hyperShade(assign=shading_group1)

    if iPathS is not None:
        shaderS = cmds.shadingNode('lambert', name='sideShader', asShader=True)
        file_nodeS = cmds.shadingNode("file", name='sTex', asTexture=True)
        cmds.setAttr(file_nodeS + '.fileTextureName', iPathS, type='string')
        shading_group2 = cmds.sets(renderable=True, noSurfaceShader=True, empty=True)

        # connect shader to sg surface shader
        cmds.connectAttr('%s.outColor' % shaderS, '%s.surfaceShader' % shading_group2)
        # connect file texture node to shader's color
        cmds.connectAttr('%s.outColor' % file_nodeS, '%s.color' % shaderS)

        createPlaneS(iPathS)

        cmds.select('sideView')
        cmds.hyperShade(assign=shading_group2)

    if iPathF is not None:
        shaderF = cmds.shadingNode('lambert', name='frontShader', asShader=True)
        file_nodeF = cmds.shadingNode("file", name='fTex', asTexture=True)
        cmds.setAttr(file_nodeF + '.fileTextureName', iPathF, type='string')
        shading_group3 = cmds.sets(renderable=True, noSurfaceShader=True, empty=True)

        # connect shader to sg surface shader
        cmds.connectAttr('%s.outColor' % shaderF, '%s.surfaceShader' % shading_group3)
        # connect file texture node to shader's color
        cmds.connectAttr('%s.outColor' % file_nodeF, '%s.color' % shaderF)

        createPlaneF(iPathF)

        cmds.select('frontView')
        cmds.hyperShade(assign=shading_group3)




class rGenUI():

    #Stuff
    def __init__(self):
        self.name = "ReferenceGenerator"
        self.size = (500, 500)

        if cmds.window(self.name, exists=True):
            cmds.deleteUI(self.name, window=True)

    #The UI
    def refWindow(self, *args):
        rWindow = cmds.window(self.name, title = 'Reference Generator', widthHeight = self.size, sizeable = False, retain=False,menuBar=True)

        self.editMenu = cmds.menu('editMenu', label='Edit')
        cmds.menuItem(label="Save Settings", parent=self.editMenu)
        cmds.menuItem(label="Reset Settings", parent=self.editMenu)

        self.helpMenu = cmds.menu('helpMenu', label='Help')
        cmds.menuItem(label="Help on Tool", parent=self.helpMenu)


        self.mainForm = cmds.formLayout('mainForm')
        self.backFrame = cmds.scrollLayout('mainScroll',hst = 16,vst = 16,borderVisible=True)

        self.rowBtn = cmds.rowLayout(numberOfColumns=2, parent=self.mainForm)
        createButton = cmds.button(label='Create', width = 250,command=self.createPlanes)
        closeButton = cmds.button(label='Close',width=250, command = ('cmds.deleteUI(\"' + rWindow + '\", window=True)'))


        cmds.formLayout(self.mainForm, edit=True, attachForm=[(self.backFrame, 'left', 0),
                                                              (self.backFrame, 'top', 0),
                                                              (self.backFrame, 'right', 0),
                                                              (self.backFrame, 'bottom', 30),
                                                              (self.rowBtn, 'bottom', 0),
                                                              (self.rowBtn, 'left', 2)])

        self.secondForm = cmds.formLayout('secondMain', parent=self.backFrame)
        self.tBtn = cmds.checkBox(label='Top', enable=True,parent=self.secondForm)
        self.tLayout = cmds.rowLayout(numberOfColumns=2, columnAttach=(1, 'left', 0), adjustableColumn=1, columnWidth2=(400, 20),enable=False)
        self.top = cmds.textField('topScenePathField',parent = self.tLayout)
        cmds.iconTextButton(style='iconAndTextVertical', command=self.scnFileOpenTop, image1='fileOpen.xpm', height=20,parent=self.tLayout)
        cmds.setParent('..')
        cmds.checkBox(self.tBtn, e=True, cc=partial(self.cBoxCheck, self.tLayout))


        self.sBtn = cmds.checkBox(label='Side', enable=True,parent=self.secondForm)
        self.sLayout = cmds.rowLayout(numberOfColumns=2, columnAttach=(1, 'left', 0), adjustableColumn=1, columnWidth2=(400, 20),enable=False)
        self.side = cmds.textField('sideScenePathField',parent=self.sLayout)
        cmds.iconTextButton(style='iconAndTextVertical', align='right', command=self.scnFileOpen2, image1='fileOpen.xpm', height=20,parent=self.sLayout)
        cmds.setParent('..')
        cmds.checkBox(self.sBtn, e=True, cc=partial(self.cBoxCheck, self.sLayout))


        self.fBtn = cmds.checkBox(label='Front')
        self.fLayout = cmds.rowLayout(numberOfColumns=2, columnAttach=(1, 'right', 0), adjustableColumn=1, columnWidth2=(400, 20),enable=False)
        self.front = cmds.textField('frontScenePathField',parent=self.fLayout)
        cmds.iconTextButton(style='iconAndTextVertical', align='right', command=self.scnFileOpen3, image1='fileOpen.xpm', height=20,parent=self.fLayout)
        cmds.setParent('..')
        cmds.checkBox(self.fBtn, e=True, cc=partial(self.cBoxCheck, self.fLayout))


        cmds.formLayout('secondMain', edit=True, attachForm=((self.tBtn, 'left', 10),
                                                            (self.tBtn, 'top', 7),
                                                            (self.tLayout, 'left', 60),
                                                            (self.tLayout, 'top', 5),
                                                            (self.sBtn, 'left', 10),
                                                            (self.sBtn, 'top', 37),
                                                            (self.sLayout, 'top', 37),
                                                            (self.sLayout, 'left', 60),
                                                            (self.fBtn, 'left', 10),
                                                            (self.fBtn, 'top', 68),
                                                            (self.fLayout, 'top', 68),
                                                            (self.fLayout, 'left', 60),
                                                             ))


        cmds.showWindow(rWindow)

#for the first text box
#TODO: clean up code so as to not have repetition
    def scnFileOpenTop(self):
        imageFilter = "Image Files (*.jpg, *.png);; JPEG Image Files (*.jpg *.jpeg)"
        chosenFile = cmds.fileDialog2(fm=1, ds=0, cap="Open", ff=imageFilter, okc="Select image file", hfe=False)
        for fPath in chosenFile:
            imageName = fPath

        cmds.textField('topScenePathField', edit=True, text=imageName)

    def scnFileOpen2(self):
        imageFilter = "Image Files (*.jpg, *.png);; JPEG Image Files (*.jpg *.jpeg)"
        chosenFile = cmds.fileDialog2(fm=1, ds=0, cap="Open", ff=imageFilter, okc="Select image file", hfe=False)
        for fPath in chosenFile:
            imageName2 = fPath

        cmds.textField('sideScenePathField', edit=True, text=imageName2)

    def scnFileOpen3(self):
        imageFilter = "Image Files (*.jpg, *.png);; JPEG Image Files (*.jpg *.jpeg)"
        chosenFile = cmds.fileDialog2(fm=1, ds=0, cap="Open", ff=imageFilter, okc="Select image file", hfe=False)
        for fPath in chosenFile:
            imageName3 = fPath

        cmds.textField('frontScenePathField', edit=True, text=imageName3)

    def cBoxCheck(self, widget, *args):
        self.currentState = cmds.rowLayout(widget, q=True, enable=False)
        cmds.rowLayout(widget, e=True, enable=(1 - self.currentState))

    #Create function for the button
    def createPlanes(self,*args):

        topV = None
        sideV = None
        frontV = None

        tBox = cmds.checkBox(self.tBtn, q=True, value=True)
        if tBox:
            topV = cmds.textField(self.top,q=True,text = True)

        sBox = cmds.checkBox(self.sBtn, q=True, value=True)
        if sBox:
            sideV = cmds.textField(self.side, q=True, text=True)

        fBox = cmds.checkBox(self.fBtn, q=True, value=True)
        if fBox:
            frontV = cmds.textField(self.front, q=True, text=True)

        applyTex(topV,sideV,frontV)

refGen = rGenUI()
refGen.refWindow()







