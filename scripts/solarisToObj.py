import hou

def cleanSubnet(Container,collectONLY=0):
        if collectONLY == 0:
                containerContents = Container.children()
                if len(containerContents) != 0:
                        for n in containerContents:
                                n.destroy()
def createNodeIfNonExistant(geoParent,geoType,geoName,setInputTo=''):
        checkExists = geoParent.node(geoName)
        ## if node does not exist create it
        if checkExists == None:
                checkExists = geoParent.createNode(geoType,geoName)
                checkExists.moveToGoodPosition(True)

        ## if setInputTo variable is given connect first input to this node
        if setInputTo != '':
                checkExists.setInput(0,setInputTo)
                checkExists.moveToGoodPosition(True)

        return checkExists
def valueTypeConvert(parameter,customVal,customValParam):
        pType = str(type(parameter.eval()))
        # print("valueTypeConvert: ")
        # print("pType: "+str(pType))
        # print("customVal: "+str(customVal))
        cPType = str(type(customValParam.eval()))
        # print("cPType: "+str(cPType))
        if pType != cPType:
                # print("pType != cPType")
                parameterValue = 'NONE'
                # print("parameterValue: "+str(parameterValue))
                return parameterValue
        if pType == cPType:
                # print("pType == cPType")
                parameterValue = 0
                if pType == "<class 'float'>":
                        parameterValue = float(customVal)
                        # print("parameterValue: "+str(parameterValue))
                        return parameterValue
                if pType == "<class 'str'>":
                        parameterValue = str(customVal)
                        # print("parameterValue: "+str(parameterValue))
                        return parameterValue
                if pType == "<class 'int'>":
                        parameterValue = int(customVal)
                        # print("parameterValue: "+str(parameterValue))
                        return parameterValue
def swapParameterName(incomingName,compareName,setName):
        incomingNameVal = str(incomingName)
        if incomingNameVal == compareName:
                incomingNameVal = setName
        return incomingNameVal
def linkLightParametersOVERRIDES(parameterName,parameterVal,lightType,renderEngine):
        parmName = parameterName
        parmVal = parameterVal
        if renderEngine == 0:
                parmName = swapParameterName(parmName,'light_texturefile','env_map')
        if renderEngine == 1:
                # if parmName == 'ar_texturefile':
                #       parmName = 'ar_light_color_texture'
                parmName = swapParameterName(parmName,'ar_texturefile','ar_light_color_texture')
                parmName = swapParameterName(parmName,'ar_textureformat','ar_format')
                parmName = swapParameterName(parmName,'ar_shadow_density','ar_shadow_density_NULL')
                if parmName == 'ar_format':
                        formatDict = {
                                'automatic':'latlong',
                                'latlong':'latlong',
                                'mirroredBall':'mirrored_ball',
                                'angular':'angular',
                                'cubeMapVerticalCross':'latlong'
                        }

                        parmVal = str(formatDict.get(parmVal))
                lightReplaceString ={           
                        'cyl':'cylinder',
                        'dist':'',
                        'disk':'disk',
                        'point':'point',
                        'rect':'quad',
                        'sphere':'point'
                }
                lightReplaceStringOut = lightReplaceString.get(str(lightType))
                if parmName == 'ar_width':
                        if lightReplaceStringOut == 'quad':
                                parmName = 'ar_quad_sizex'
                if parmName == 'ar_height':
                        if lightReplaceStringOut == 'quad':
                                parmName = 'ar_quad_sizey'
                if parmName == 'ar_length':
                        parmName = 'ar_height'
                if parmName == 'ar_radius':
                        parmName = 'ar_'+str(lightReplaceStringOut)+'_radius'
                        if str(parmName) == 'ar_point_radius':
                                parmVal = '0'
        outValues = [parmName,parmVal]
        return outValues
def linkLightParameters(pullNode,setNode,renderEngine,domeLight=0):
        renderEngine = renderEngine
        lightLinkNode = setNode
        lightEvalNode = pullNode
        replaceInputParmName = ['light_','ar_','Light1']
        replaceInputShadowParmName = ['shadow_','ar_shadow_','Light1_shadow']
        LopLightTypeDict = { 
                '0':'cyl',
                '1':'dist',
                '2':'disk',
                '3':'point',
                '4':'rect',
                '5':'sphere'
        }
        OBJLightTypeDict = { 
                'cyl':'5/5/3',
                'dist':'7/1/0',
                'disk':'3/4/3',
                'point':'0/0/1',
                'rect':'2/3/3',
                'sphere':'4/0/3'
        }
        parmDictionary = {}
        parmSourceDictionary = {}
        normalize = 0
        if domeLight == 0:
                lightTypeEvaluate = lightEvalNode.parm('lighttype').eval()
                lightTypeEvaluate = LopLightTypeDict.get(str(lightTypeEvaluate))
        if domeLight == 1:
                lightTypeEvaluate = '6'
        for param in hou.Node.globParms(lightEvalNode,"*"):
                paramSource = param
                pVal = param.eval()
                pName = param.name()
                pRawName = pName
                pName = pName.replace('xn__','')
                pName = pName.replace('primvars','')
                if renderEngine == 1:
                        passThrough = 0
                        if 'control' in pName:
                                passThrough = 1
                        if passThrough == 0:
                                pName = pName.replace('arnold:','ar_')
                                pName = pName.replace('arnold','ar_')
                if renderEngine == 0:
                        pName = pName.replace('karma:light:','')
                if renderEngine == 2:
                        pName = pName.replace('redshift:','')
                        pName = pName.replace('redshift','')
                # pName = pName.replace('inputsshadow','')
                # pName = pName.replace('inputsshaping','')
                pName = pName.replace('inputs','inputs/')
                pName = pName.replace('inputs/shadow','NA/')
                pName = pName.replace('inputs/shaping','NA/')
                # pName = pName.replace('inputsshadow/',replaceInputShadowParmName[renderEngine])
                pName = pName.replace('inputs/',replaceInputParmName[renderEngine])
                if '_' in pName:

                        popName = '_'+(pName.split('_')).pop()
                        if popName != '_control':
                                pName = pName.replace(popName,'')

                pName.replace(':','')

                if pRawName == 'lighttype':
                        pName = ['light_type','ar_light_type','light_type']
                        pName = pName[renderEngine]

                        pVal = LopLightTypeDict.get(str(pVal))

                        lightTypeString = pVal

                        if lightTypeString == 'point' and renderEngine == 1:
                                normalize = 1

                        pVal = (str(OBJLightTypeDict.get(str(pVal))).split('/'))[renderEngine]

                lightTypePull = lightTypeEvaluate
                pName = linkLightParametersOVERRIDES(pName,pVal,lightTypePull,renderEngine)
                if pName[1] != '':
                        pVal = str(pName[1])
                parmDictionary[pName[0]]=pVal
                parmSourceDictionary[pName[0]]=paramSource

        for paramLink in hou.Node.globParms(lightLinkNode,"*"):

                lightLinkParm = paramLink.name()
                # print("lightLinkParm: "+lightLinkParm)

                getLink = parmDictionary.get(lightLinkParm)
                # print("getLink: "+str(getLink))
                getSource = parmSourceDictionary.get(lightLinkParm)
                # print("getSource: "+str(getSource))


                if getLink != None:
                        setParameterValue = valueTypeConvert(paramLink,getLink,getSource)
                        # print("setParameterValue: "+str(setParameterValue))

                        if setParameterValue != 'NONE':
                                if lightLinkParm == 'ar_normalize':
                                        setParameterValue = normalize
                                try:
                                    lightLinkNode.parm(lightLinkParm).set(setParameterValue)
                                except TypeError:
                                    print('trouble linking- parm:'+str(lightLinkParm)+' to value of: '+str(setParameterValue))
def createMaterialNode(Container,nodeType,nodeName,renderEngine,setInputTo=''):
        setInputList = setInputTo
        if setInputTo == '':
                setInputList = ['','','','','','','']
        outputNode_S = createNodeIfNonExistant(Container,nodeType[renderEngine],nodeName[renderEngine],setInputList[renderEngine])
        return outputNode_S
def materialSetup(materialContainter='',renderEngine=3,collectONLY=0):

        ## Surface Nodes Name/Type/Connections
        surfaceName = ['mtlxstandard_surface','standard_surface1','StandardMaterial1','NONE']
        surfaceNode_type = ['mtlxstandard_surface','arnold::standard_surface','redshift::StandardMaterial']
        surfaceNode_connect = ['','','','']
        ##SET -- NODE
        if collectONLY == 0:
                surfaceNode = createMaterialNode(materialContainter,surfaceNode_type,surfaceName,renderEngine,surfaceNode_connect)
                ## Surface Nodes Parameters
                roughnessParameterLabel = ['specular_roughness','specular_roughness','refl_roughness','']
                ##      Set -- PARMS
                surfaceNode.parm(roughnessParameterLabel[renderEngine]).set(0.5)

        ## Output Nodes Name/Type/Connections
        outputName = ['surface_output','OUT_material','redshift_usd_material1','NONE']
        outputNode_type = ['subnetconnector','arnold_material','redshift_usd_material']
        outputNode_connect = [surfaceNode,surfaceNode,surfaceNode,'']
        ##SET -- NODE
        if collectONLY == 0:
                outputCollectNode = createMaterialNode(materialContainter,outputNode_type,outputName,renderEngine,outputNode_connect)
def createMtlXSubnet(Container):
        nodeChildren = Container.children()
        for child in nodeChildren:
                childName = child.name()
                if childName == 'subinput1':
                        child.destroy()
                if childName == 'suboutput1':
                        child.destroy()

        mtlxSurf = createNodeIfNonExistant(Container,'mtlxstandard_surface','mtlxstandard_surface')
        mtlxDisplacement = createNodeIfNonExistant(Container,'mtlxdisplacement','mtlxdisplacement')

        surfaceOutput = createNodeIfNonExistant(Container,'subnetconnector','surface_output',mtlxSurf)
        surfaceOutput.parm('connectorkind').set('output')
        surfaceOutput.parm('parmname').set('surface')
        surfaceOutput.parm('parmlabel').set('Surface')
        surfaceOutput.parm('parmtype').set('surface')

        displacementOutput = createNodeIfNonExistant(Container,'subnetconnector','displacement_output',mtlxDisplacement)
        displacementOutput.parm('connectorkind').set('output')
        displacementOutput.parm('parmname').set('displacement')
        displacementOutput.parm('parmlabel').set('Displacement')
        displacementOutput.parm('parmtype').set('displacement')
        Container.setMaterialFlag(True)
def sortThroughNodes(nodeType,camUse=0,Container='/obj',inIfUse=0):
        obj = hou.node(Container)
        stage = hou.node('/stage')

        camTypes = ['AX_MultiShot','ax_camera','cam']

        allNodes = obj.children()
        collectedNodes = []
        if camUse == 0:
                for n in allNodes:
                        nType = n.type().name()
                        if inIfUse == 0:
                                if nodeType == nType:
                                        collectedNodes.append(n)
                        if inIfUse == 1:
                                if nodeType in nType:
                                        collectedNodes.append(n)
        if camUse == 1:
                for n in allNodes:
                        nType = n.type().name()
                        for cType in camTypes:
                                if cType in nType:
                                        collectedNodes.append(n)
        return collectedNodes
def setupCameras(importCamera,collectONLY=0):
        obj = hou.node('/obj')  
        stage = hou.node('/stage')
        sceneImportNode = createNodeIfNonExistant(stage,'sceneimport','ImportScene')
        importNodeEval = importCamera
        importNodeName = importNodeEval.name()
        importNodePath = importNodeEval.path()
        objNetwork = createNodeIfNonExistant(stage,'objnet','importGeometry')
        nodeName = importNodeName
        nodePath = importNodePath
        nodeInputs = importNodeEval.inputs()
        parent_tx = '0'
        parent_ty = '0'
        parent_tz = '0'
        parent_rx = '0'
        parent_ry = '0'
        parent_rz = '0'
        parent_scale = '1'
        ## Check for input nulls
        if str(nodeInputs) != '()':
                if collectONLY == 0:
                        nodeParent = nodeInputs[0]
                        nodeParentPath = nodeParent.path()
                        parent_tx = str(nodeParent.parm('tx').eval())
                        parent_ty = str(nodeParent.parm('ty').eval())
                        parent_tz = str(nodeParent.parm('tz').eval())
                        parent_rx = str(nodeParent.parm('rx').eval())
                        parent_ry = str(nodeParent.parm('ry').eval())
                        parent_rz = str(nodeParent.parm('rz').eval())
                        parent_scale = str(nodeParent.parm('scale').eval())            
        ## Create Camera
        newCam = createNodeIfNonExistant(objNetwork,'cam',nodeName)
        lopCam = createNodeIfNonExistant(stage,'camera',nodeName+"_edit",sceneImportNode)
        ##link translates
        if collectONLY == 0:
                newCam.parm('tx').setExpression("ch('"+nodePath+"/tx')"+"*"+parent_scale+"+"+parent_tx)
                newCam.parm('ty').setExpression("ch('"+nodePath+"/ty')"+"*"+parent_scale+"+"+parent_ty)
                newCam.parm('tz').setExpression("ch('"+nodePath+"/tz')"+"*"+parent_scale+"+"+parent_tz)
                ##link rotates
                newCam.parm('rx').setExpression("ch('"+nodePath+"/rx')"+"+"+parent_rx)
                newCam.parm('ry').setExpression("ch('"+nodePath+"/ry')"+"+"+parent_ry)
                newCam.parm('rz').setExpression("ch('"+nodePath+"/rz')"+"+"+parent_rz)
                ##link resolution
                newCam.parm('resx').setExpression("ch('"+nodePath+"/resx')")
                newCam.parm('resy').setExpression("ch('"+nodePath+"/resy')")
                ##link focal and apeture
                newCam.parm('focal').setExpression("ch('"+nodePath+"/focal')")
                newCam.parm('aperture').setExpression("ch('"+nodePath+"/aperture')")
                newCam.parm('fstop').set(50000) ## set BG super high to avoid DOF
                ##link background image
                newCam.parm('vm_background').setExpression("chs('"+nodePath+"/vm_background')")
                lopCam.parm('createprims').set("off")
                lopCam.parm('primpattern').set("/"+nodeName)
                lopCam.parm('initforedit').pressButton()
                lopCam.parm('xn__houdinibackgroundimage_control_ypb').set("set")
                lopCam.parm('xn__houdinibackgroundimage_xcb').setExpression("chs('"+nodePath+"/vm_background')")

        newCam.moveToGoodPosition(True)
def setupMaterials(renderEngine=3,materialName='',materialContainer='',collectONLY=0):
        renderTypeList = ['subnet','arnold_materialbuilder','rs_usd_material_builder','']
        renderType = renderTypeList[renderEngine]
        if renderType != '':
                material = createNodeIfNonExistant(materialContainer,renderType,materialName)
                if renderEngine == 0:
                        if collectONLY == 0:
                                createMtlXSubnet(material)
                materialSetup(material,renderEngine,collectONLY=collectONLY)
        return material
def setupNodes(importNode,renderEngine=3,collectONLY=0):
        obj = hou.node('/obj')
        stage = hou.node('/stage')

        objNetwork = createNodeIfNonExistant(stage,'objnet','importGeometry')
        matNetwork = createNodeIfNonExistant(stage,'matnet','materialNetwork')

        importNodeName = importNode.name()
        importNodePath = importNode.path()

        connectingMatNode = setupMaterials(renderEngine,importNodeName+'_MATERIAL',matNetwork,collectONLY=collectONLY)

        importGeoContainer = createNodeIfNonExistant(objNetwork,'geo','import_'+importNodeName)

        sceneImportNode = createNodeIfNonExistant(stage,'sceneimport','ImportScene')
        if collectONLY == 0:
                sceneImportNode.parm('rootobject').set(objNetwork.path())
                sceneImportNode.parm('objects').set('/stage/importGeometry/*')
                sceneImportNode.parm('enable_packedhandling').set(1)
                sceneImportNode.parm('packedhandling').set('pointinstancer')
                sceneImportNode.parm('importmats').set(1)

        # stagePull = createNodeIfNonExistant(stage,'null','COLLECT_LIGHTS',sceneImportNode)

        objMergeGeo = createNodeIfNonExistant(importGeoContainer,'object_merge','object_merge')
        if collectONLY == 0:
                objMergeGeo.parm('xformtype').set('local')
                objMergeGeo.parm('objpath1').set(importNodePath)


        groupDelete = createNodeIfNonExistant(importGeoContainer,'groupdelete','groupdelete',objMergeGeo)
        if collectONLY == 0:
                groupDelete.parm('group1').set('*')

        attribDelete = createNodeIfNonExistant(importGeoContainer,'attribdelete','attribdelete',groupDelete)
        if collectONLY == 0:
                attribDelete.parm('negate').set(1)
                attribDelete.parm('ptdel').set('width pscale')
                attribDelete.parm('vtxdel').set('uv')

        normalNode = createNodeIfNonExistant(importGeoContainer,'normal','normal',attribDelete)

        matNode = createNodeIfNonExistant(importGeoContainer,'material','material',normalNode)
        if collectONLY == 0:
                matNode.parm('shop_materialpath1').set(connectingMatNode.path())

        nameNode = createNodeIfNonExistant(importGeoContainer,'name','rename',matNode)
        if collectONLY == 0:
                nameNode.parm('name1').set(importNodeName)

        nullOut = createNodeIfNonExistant(importGeoContainer,'null','OUT',nameNode)
        if collectONLY == 0:
                nullOut.setDisplayFlag(True)
                nullOut.setRenderFlag(True)
def loopOverFoundNodes(renderEngine=3,collectONLY=0):
        foundNodes = sortThroughNodes('geo')
        for n in foundNodes:
            flagRead = n.isDisplayFlagSet()
            if flagRead == True:
                        setupNodes(n,renderEngine,collectONLY=collectONLY)
        foundCams = sortThroughNodes('cam',camUse=1)
        for c in foundCams:
                setupCameras(c,collectONLY=collectONLY)
def runSetup():
        obj = hou.node('/obj')
        stage = hou.node('/stage')
        
        renderEngine = hou.ui.displayMessage( 'Render Engine:',buttons=('Mantra/Karma','Arnold','Redshift','Cancel'),default_choice=(3),close_choice=(3))
        importExport = hou.ui.displayMessage( 'Send/Build:',buttons=('Send to Solaris','Build from Solaris','Cancel'),default_choice=(2),close_choice=(2))
        objLightType = ['hlight','arnold_light','rslight']
        objLightDomeType = ['envlight','arnold_light','rslightdome']
        objLightType = objLightType[renderEngine]
        objLightDomeType = objLightDomeType[renderEngine]
        lgtSelect = None
        if importExport == 0:
                objNetwork = createNodeIfNonExistant(stage,'objnet','importGeometry')
                matNetwork = createNodeIfNonExistant(stage,'matnet','materialNetwork')
                cleanSubnet(matNetwork)
                sceneImportNode = createNodeIfNonExistant(stage,'sceneimport','ImportScene')
                loopOverFoundNodes(renderEngine)
                desktops_dict = dict((d.name(), d) for d in hou.ui.desktops())
                desktops_dict['Solaris'].setAsCurrent()
                lgtSelect = sceneImportNode
        if importExport == 1:
                objNetwork = createNodeIfNonExistant(stage,'objnet','importGeometry')
                matNetwork = createNodeIfNonExistant(stage,'matnet','materialNetwork')
                useMats = hou.ui.displayMessage('Use Materials:',buttons=('Do Nothing','Bring Materials'),default_choice=(0))
                if useMats == 1:
                        geoNodes = objNetwork.children()
                        for gN in geoNodes:
                                if gN.type().name() == 'geo':
                                        importNodePath = gN.node('object_merge').parm('objpath1').eval()
                                        importNodeMaterialPath = gN.node('material').parm('shop_materialpath1').eval()
                                        hou.node(importNodePath).parm('shop_materialpath').set(importNodeMaterialPath)
                lights = sortThroughNodes('light::2.0',Container='/stage',inIfUse=0)
                if len(lights) != 0:
                        for l in lights:
                                lightName = l.name()
                                newObjLight = createNodeIfNonExistant(obj,objLightType,lightName)
                                lgtSelect = newObjLight
                                linkLightParameters(l,newObjLight,renderEngine,domeLight=0)
                lightDomes = sortThroughNodes('domelight',Container='/stage',inIfUse=1)
                if len(lights) != 0:
                        for lgtD in lightDomes:
                                lightDomeName = lgtD.name()
                                lightDomeFormat = lgtD.parm('xn__inputstextureformat_06ah').eval()
                                newObjLightDome = createNodeIfNonExistant(obj,objLightDomeType,lightDomeName)
                                lgtSelect = newObjLightDome
                                if renderEngine == 1:
                                        formatDict = {
                                                'automatic':'latlong',
                                                'latlong':'latlong',
                                                'mirroredBall':'mirrored_ball',
                                                'angular':'angular',
                                                'cubeMapVerticalCross':'latlong'
                                        }
                                        lightDomeFormat = str(formatDict.get(lightDomeFormat))
                                        newObjLightDome.parm('ar_format').set(lightDomeFormat)
                                        newObjLightDome.parm('ar_light_type').set(6)
                                        newObjLightDome.parm('ar_light_color_type').set(1)
                                        
                                linkLightParameters(lgtD,newObjLightDome,renderEngine,domeLight=1)
                desktops_dict = dict((d.name(), d) for d in hou.ui.desktops())
                desktops_dict['Build'].setAsCurrent()
        if lgtSelect != None:
                lgtSelect.setCurrent(True,clear_all_selected=True)
        if lgtSelect == None:
                lgtSelect = (obj.children())[0]
                lgtSelect.setCurrent(True,clear_all_selected=True)
runSetup()