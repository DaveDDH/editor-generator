from IOUtils import createDirInDisk, listAllFilesFromList, copyFile, readAllFilesInDiskDir, readFileFromDisk, writeFileToDisk
from JSONUtils import transformJSONSIntoObjects

def copyTemplateAssetFiles(templateAssets, mDirPath):
    assetsToCopyArrStr = templateAssets.split(',')
    assetsToCopyArrStr = ["./static/" + x for x in assetsToCopyArrStr]
    assetsToCopySrc = listAllFilesFromList(assetsToCopyArrStr)
    assetsToCopyDst = [x[14:] for x in assetsToCopySrc]
    assetsLen = len(assetsToCopySrc)
    for i in range(assetsLen):
        copyFile(assetsToCopySrc[i], mDirPath + "/" + assetsToCopyDst[i])

def copyServerFiles(serverFiles, mDirPath):
    filesToCopyArrStr = serverFiles.split(',')
    filesToCopyArrStr = ["./static/" + x for x in filesToCopyArrStr]
    filesToCopySrc = listAllFilesFromList(filesToCopyArrStr)
    filesToCopyDst = [x[15:] for x in filesToCopySrc]
    filesLen = len(filesToCopySrc)
    for i in range(filesLen):
        copyFile(filesToCopySrc[i], mDirPath + "/" + filesToCopyDst[i])

def personalizeServerDBConnection(connectionString, mDirPath):
    mContent = readFileFromDisk(mDirPath + '/secrets/mongocreds.js')
    mContent = mContent.replace('{{connectionString}}', connectionString)
    writeFileToDisk(mDirPath + '/secrets/', 'mongocreds.js', mContent)

def createNavigationFormHTMLForHome(properties, artifacts):
    html = ""
    template = properties['templateNavigationFormHTMLForHome']
    for artifact in artifacts:
        mTem = template
        artifactName = artifact['name']
        artifactType = artifact['type']
        if artifactType  == 'bac':
            mTem = mTem.replace("{{formHTMLPath}}", artifactName + ".html")
            mTem = mTem.replace("{{formName}}", artifactName)
            html += mTem + "\n"
    alreadySetQueryHeader = False
    for artifact in artifacts:
        mTem = template
        artifactName = artifact['name']
        artifactType = artifact['type']
        if artifactType  == 'query':
            if not alreadySetQueryHeader:
                alreadySetQueryHeader = True
                html += '<li class="app-sidebar__heading">Queries</li>'
            mTem = mTem.replace("{{formHTMLPath}}", 'query-' + artifactName + ".html")
            mTem = mTem.replace("{{formName}}", artifactName)
            html += mTem + "\n"
    return html

def createNavigationFormHTMLForForm(properties, artifacts, active):
    html = ""
    template = properties['templateNavigationFormHTMLForForm']
    for artifact in artifacts:
        mTem = template
        artifactName = artifact['name']
        artifactType = artifact['type']
        if artifactType  == 'bac':
            mActive = ""
            if artifactName == active:
                mActive = 'class="mm-active"'
            mTem = mTem.replace("{{active}}", mActive)
            mTem = mTem.replace("{{formHTMLPath}}", artifactName + ".html")
            mTem = mTem.replace("{{formName}}", artifactName)
            html += mTem + "\n"
    alreadySetQueryHeader = False
    for artifact in artifacts:
        mTem = template
        artifactName = artifact['name']
        artifactType = artifact['type']
        if artifactType  == 'query':
            if not alreadySetQueryHeader:
                alreadySetQueryHeader = True
                html += '<li class="app-sidebar__heading">Queries</li>'
            mActive = ""
            if artifactName == active:
                mActive = 'class="mm-active"'
            mTem = mTem.replace("{{active}}", mActive)
            mTem = mTem.replace("{{formHTMLPath}}", 'query-' + artifactName + ".html")
            mTem = mTem.replace("{{formName}}", artifactName)
            html += mTem + "\n"
    return html


def createFormHTML(formTemplate, name, properties, artifacts, artifact):
    navigationFormHTML = createNavigationFormHTMLForForm(properties, artifacts, name)
    mTem = formTemplate
    mTem = mTem.replace("{{name}}", name)
    mTem = mTem.replace("{{description}}", artifact['description'])
    mTem = mTem.replace("{{forms}}", navigationFormHTML)
    mTem = mTem.replace("{{formName}}", name)
    tableHeadContent = ""
    formHeaders = ""
    mainSection = artifact['mainSection']
    for section in artifact['sections']:
        if section['sectionName'] == mainSection:
            for field in section['fields']:
                tableHeadContent += "<th>" + field['fieldName'] + "</th>"
                formHeaders += field['fieldName'] + ","
    formHeaders += "Options"
    tableHeadContent += "<th>Options</th>"
    mTem = mTem.replace("{{mainSectionName}}", mainSection)
    mTem = mTem.replace("{{formHeaders}}", formHeaders)
    mTem = mTem.replace("{{tableHeadContent}}", tableHeadContent)
    return mTem

def createQueryHTML(formTemplate, name, properties, artifacts, artifact):
    navigationFormHTML = createNavigationFormHTMLForForm(properties, artifacts, name)
    mTem = formTemplate
    mTem = mTem.replace("{{name}}", name)
    mTem = mTem.replace("{{description}}", artifact['description'])
    mTem = mTem.replace("{{forms}}", navigationFormHTML)
    mTem = mTem.replace("{{formName}}", name)
    mQuery = artifact['query']
    mTem = mTem.replace("{{query}}", mQuery)
    
    return mTem

def createDetailViewHTML(formTemplate, name, properties, artifacts, artifact):
    navigationFormHTML = createNavigationFormHTMLForForm(properties, artifacts, name)
    mTem = formTemplate
    mTem = mTem.replace("{{name}}", name)
    mTem = mTem.replace("{{description}}", artifact['description'])
    mTem = mTem.replace("{{forms}}", navigationFormHTML)
    mTem = mTem.replace("{{formName}}", name)
    tableHeadContent = ""
    formHeaders = "{\n"
    mainSection = artifact['mainSection']
    for section in artifact['sections']:
        mRealSection = section
        if section['fields'][0]['amount'] == 'many':
            mRealSection = section['fields'][0]
        mSection = section['sectionName']
        mForm = mSection.replace(" ", "") + ": '"
        mTableHeadContent = '<div class="sectionTitle">' + mSection + '</div><table id="example{{sectionName}}" class="display" style="width:100%"><thead><tr>'
        mTableHeadContent = mTableHeadContent.replace("{{sectionName}}", mSection.replace(" ", ""))
        for field in mRealSection['fields']:
            mTableHeadContent += "<th>" + field['fieldName'] + "</th>"
            mForm += field['fieldName'] + ","
        mTableHeadContent += "<th>Options</th>"
        mTableHeadContent += '</tr></thead><tbody id="tableBody{{sectionName}}"></tbody></table>\n'
        mTableHeadContent = mTableHeadContent.replace("{{sectionName}}", mSection.replace(" ", ""))
        mForm += "Options"
        mForm += "',\n"
        formHeaders += mForm
        tableHeadContent += mTableHeadContent
    formHeaders += '};'
    tableHeadContent += ''
    mTem = mTem.replace("{{mainSectionName}}", mainSection)
    mTem = mTem.replace("{{formHeaders}}", formHeaders)
    mTem = mTem.replace("{{tableHeadContent}}", tableHeadContent)
    return mTem


def createContentFormHTMLForForm(properties, artifact, scripts, artifacts):
    html = ""
    name = artifact['name']
    mainSection = artifact['mainSection']
    for section in artifact['sections']:
        mTemp = properties['templateFormUp'].replace("{{sectionName}}", section['sectionName'])
        html += mTemp
        wasJS = False
        mFields = section['fields']
        for field in mFields:
            many = field['amount']
            if field['amount'] == "many":
                mStrJson = str(field).replace("'", '&quot;').replace('\n', "")
                html = html[:len(html) - len(mTemp)]
                mmmHtml = properties['templateFormJS'].replace("{{sectionName}}", section['sectionName'])
                wasJS = True
                html += mmmHtml + '</div><div><div onclick="' + "addNewField('" + mStrJson + "', '" + section['sectionName'] + "')" + '" style="width:max-content;font-size: 14px;color: green;cursor: pointer;border: 1px solid green;padding: 4px 12px 4px 12px;border-radius: 5px; cursor:pointer;">Añadir ' + section['sectionName'] + '</div></div>'
                many = 1
            else:
                amount = int(many)
                for i in range(amount):
                    if 'fields' in field:
                        html += recursivelyCreateContentFormHTMLForForm(properties, field, 1, True, scripts, section['sectionName'], artifacts)
                    else:
                        mAddID = ""
                        mAddName = ""
                        if amount > 1:
                            mAddID = str(i + 1)
                            mAddName = " " + str(i + 1)
                        if field['fieldName'].find('.') != -1:
                            mArtefactName = field['fieldName'].split('.')[0]
                            mForm = properties['templateFormFieldSelect']
                            mForm = mForm.replace("{{fieldID}}", field['fieldName'] + mAddID)
                            mForm = mForm.replace("{{fieldName}}", field['fieldName'] + mAddName)
                            mForm = mForm.replace("{{sectionName}}", section['sectionName'])
                            mForm += "<script>"
                            mForm += "mDataToPopulate.push('" + str(field['fieldName'] + mAddID) + ":" + section['sectionName'] + "');"
                            mMainSec = ""
                            for mArt in artifacts:
                                if mArt['name'] == mArtefactName:
                                    mMainSec = mArt['mainSection']
                            mForm += "mMainSections['" + mArtefactName + "'] = '" + mMainSec + "';"
                            mForm += "</script>"
                            html += mForm
                        else:
                            if field['type'].find('file/') == 0:
                                mTypes = field['type'][5:]
                                mForm = properties['templateFormFieldFile']
                                mForm = mForm.replace("{{fieldID}}", field['fieldName'] + mAddID)
                                mForm = mForm.replace("{{fieldName}}", field['fieldName'] + mAddName)
                                mForm = mForm.replace("{{sectionName}}", section['sectionName'])
                                mForm = mForm.replace("{{acceptType}}", mTypes)
                                mForm += "<script>"
                                mForm += "mFileIds.push('" + str(field['fieldName'] + mAddID) + "');"
                                mForm += "</script>"
                                html += mForm
                            else:
                                if field['type'].find('|') != -1:
                                    mForm = properties['templateFormFieldSelect']
                                    mForm = mForm.replace("{{fieldID}}", field['fieldName'] + mAddID)
                                    mForm = mForm.replace("{{fieldName}}", field['fieldName'] + mAddName)
                                    mForm = mForm.replace("{{sectionName}}", section['sectionName'])
                                    mFormOptions = ""
                                    mForms = field['type'].split('|')
                                    for i in range(len(mForms)):
                                        mFormOptions += "<option>" + mForms[i] + "</option>"
                                    mForm = mForm.replace("{{formOptions}}", mFormOptions)
                                    html += mForm
                                else:
                                    mForm = properties['templateFormField']
                                    mForm = mForm.replace("{{fieldID}}", field['fieldName'] + mAddID)
                                    mForm = mForm.replace("{{placeholder}}", field['fieldName'])
                                    mForm = mForm.replace("{{fieldName}}", field['fieldName'] + mAddName)
                                    mForm = mForm.replace("{{sectionName}}", section['sectionName'])
                                    html += mForm
        button = properties['templateFormButton'].replace("{{formName}}", "'" + name + "'").replace("{{sectionName}}", "'" + section['sectionName'] + "'")
        if wasJS:
            html += button + properties['templateFormDownJS']
        else:
            html += button + properties['templateFormDown']
    return html 

def recursivelyCreateContentFormHTMLForForm(properties, artifact, num, showName, scripts, sectionName, artifacts):
    mNam = ""
    mMany = False
    if showName:
        mNam = artifact['fieldName']
    html = mNam + '<div style="margin-left:' + str(num * 30) + 'px;">'
    mFields = artifact['fields']
    for field in mFields:
        many = field['amount']
        if field['amount'] == "many":
            mMany = True
            html += field['fieldName'] + '<div onclick="addNewField()" style="font-size: 20px;color: green;cursor: pointer;">+</div>'
            many = 1
        amount = int(many)
        for i in range(amount):
            if 'fields' in field:
                html += recursivelyCreateContentFormHTMLForForm(properties, field, num + 1, not many, scripts, sectionName, artifacts)
            else:
                mAddID = ""
                mAddName = ""
                if amount > 1:
                    mAddID = str(i + 1)
                    mAddName = " " + str(i + 1)
                if field['fieldName'].find('.') != -1:
                    mForm = properties['templateFormFieldSelect']
                    mForm = mForm.replace("{{sectionName}}", sectionName)
                    mForm = mForm.replace("{{fieldID}}", field['fieldName'] + mAddID)
                    mForm = mForm.replace("{{placeholder}}", field['fieldName'])
                    mForm = mForm.replace("{{fieldName}}", field['fieldName'] + mAddName)
                    mForm += "<script>"
                    mForm += "mDataToPopulate.push('" + str(field['fieldName'] + mAddID) + ":" + sectionName + "');"
                    mForm += "</script>"
                    html += mForm
                else:
                    mForm = properties['templateFormField']
                    mForm = mForm.replace("{{sectionName}}", sectionName)
                    mForm = mForm.replace("{{fieldID}}", field['fieldName'] + mAddID)
                    mForm = mForm.replace("{{placeholder}}", field['fieldName'])
                    mForm = mForm.replace("{{fieldName}}", field['fieldName'] + mAddName)
                    html += mForm
    html += "</div>"
    return html

def createCreateFormTemplate(formTemplate, name, properties, artifacts, artifact):
    navigationFormHTML = createNavigationFormHTMLForForm(properties, artifacts, name)
    mTem = formTemplate
    mTem = mTem.replace("{{name}}", name)
    mTem = mTem.replace("{{description}}", artifact['description'])
    mTem = mTem.replace("{{forms}}", navigationFormHTML)
    mTem = mTem.replace("{{formName}}", name)
    scripts = []
    contentFormHTML = createContentFormHTMLForForm(properties, artifact, scripts, artifacts)
    mTem = mTem.replace("{{content}}", contentFormHTML)
    return mTem

def createTemplateFiles(name, dir, properties, artifacts):
    navigationFormHTML = createNavigationFormHTMLForHome(properties, artifacts)
    mainTemplateStr = properties['mainTemplate']
    mainTemplate = readFileFromDisk(mainTemplateStr)
    mainTemplate = mainTemplate.replace("{{name}}", name)
    mainTemplate = mainTemplate.replace("{{description}}", properties['templateDescription'])
    mainTemplate = mainTemplate.replace("{{forms}}", navigationFormHTML)
    writeFileToDisk(dir, "index.html", mainTemplate)

    formTemplateStr = properties['formTemplate']
    formTemplate = readFileFromDisk(formTemplateStr)

    createFormTemplateStr = properties['createFormTemplate']
    createFormTemplate = readFileFromDisk(createFormTemplateStr)

    editTemplateStr = properties['editTemplate']
    editTemplate = readFileFromDisk(editTemplateStr)

    createDetailTemplateStr = properties['detailTemplate']
    createDetailTemplate = readFileFromDisk(createDetailTemplateStr)

    queryTemplateStr = properties['queryTemplate']
    queryTemplate = readFileFromDisk(queryTemplateStr)

    for artifact in artifacts:
        artifactName = artifact['name']
        artifactType = artifact['type']
        if artifactType  == 'bac':
            formHTML = createFormHTML(formTemplate, artifactName, properties, artifacts, artifact)
            writeFileToDisk(dir, artifactName + ".html", formHTML)

            formCreateHTML = createCreateFormTemplate(createFormTemplate, artifactName, properties, artifacts, artifact)
            writeFileToDisk(dir, "create-" + artifactName + ".html", formCreateHTML)

            editHTML = createCreateFormTemplate(editTemplate, artifactName, properties, artifacts, artifact)
            writeFileToDisk(dir, "edit-" + artifactName + ".html", editHTML)

            detailViewHTML = createDetailViewHTML(createDetailTemplate, artifactName, properties, artifacts, artifact)
            writeFileToDisk(dir, "view-" + artifactName + ".html", detailViewHTML)
        elif artifactType == 'query':
            queryHTML = createQueryHTML(queryTemplate, artifactName, properties, artifacts, artifact)
            writeFileToDisk(dir, 'query-' + artifactName + ".html", queryHTML)


def generate(properties, args):
    name = args['name']
    mDirPath = createDirInDisk(args['output'], name)
    if mDirPath != False:
        mDirPathHTML = createDirInDisk(mDirPath, 'web')
        mDirPathServer = createDirInDisk(mDirPath, 'server')
        copyTemplateAssetFiles(properties['templateAssets'], mDirPathHTML)
        copyServerFiles(properties['serverFiles'], mDirPathServer)
        personalizeServerDBConnection(properties['mongodbConnectionString'], mDirPathServer)
        artifactsDir = args['artifactsDir']
        files = readAllFilesInDiskDir(artifactsDir, ".json")
        artifacts = transformJSONSIntoObjects(files)
        createTemplateFiles(name, mDirPathHTML, properties, artifacts)
    else:
        print("ERROR: the output directory already exists.")
