"use strict";
(self["webpackChunkpost_ext_web"] = self["webpackChunkpost_ext_web"] || []).push([["lib_index_js"],{

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/services */ "webpack/sharing/consume/default/@jupyterlab/services");
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/filebrowser */ "webpack/sharing/consume/default/@jupyterlab/filebrowser");
/* harmony import */ var _jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_2__);



/**
 * Initialization data for the post_ext_web extension.
 */
const webPath = '/mnt/tljhweb';
const URL = 'https://tljhweb.ictsoeasy.co.uk';
let session = null; // Global session variable
const webify_command = 'webify:webify';
const plugin = {
    id: 'post_ext_web:plugin',
    description: 'A JupyterLab extension to post a folder to an external website.',
    autoStart: true,
    requires: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.ICommandPalette, _jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_2__.IFileBrowserFactory],
    activate: (app, palette, fileBrowserFactory) => {
        console.log('JupyterLab extension post_ext_web is activated!');
        const { tracker } = fileBrowserFactory;
        app.commands.addCommand(webify_command, {
            label: 'Webify',
            caption: 'Webify',
            execute: async (args) => {
                //console.log('Args:'+args);
                const widget = tracker.currentWidget;
                if (!widget) {
                    console.log('No widget');
                    return;
                }
                const path = widget.selectedItems().next();
                //console.log(JSON.stringify(path, null, 2));
                console.log('We are going to move:' + path.value.path);
                const localPath = path.value.path;
                moveFilesForWebify(localPath);
            }
        });
        const category = 'WHO';
        palette.addItem({ command: webify_command, category, args: { origin: 'from palette' } });
        // Add the command to the file browser context menu, limited to directories
        app.contextMenu.addItem({
            command: webify_command,
            selector: '.jp-DirListing-item[data-isdir="true"]',
            rank: 10
        });
    }
};
async function moveFilesForWebify(localPath) {
    // Identify student's name
    const currentURL = window.location.href;
    console.log("Current URL:", currentURL);
    const urlParts = window.location.pathname.split('/');
    const userIndex = urlParts.indexOf('user');
    const username = userIndex !== -1 ? urlParts[userIndex + 1] : "Unknown User";
    console.log("Current Username:", username);
    const codeRun = await runCode(generatePythonCode(webPath, username, localPath))
        .catch(error => {
        console.log('Error running code:', error);
    });
    console.log('Code run:' + codeRun);
    console.log('All finished');
    window.open(URL + '/' + username, '_blank');
}
function generatePythonCode(webPath, userName, localPath) {
    var code = `import os
import shutil
path = '` + webPath + `'
def copy_folder_contents(src, dest):
    # Ensure the destination directory exists
    os.makedirs(dest, exist_ok=True)

    # Copy each item within the source directory to the destination
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dest, item)
        if os.path.isdir(s):
            shutil.copytree(s, d)  # Copy subdirectory and its contents
        else:
            shutil.copy2(s, d)     # Copy file

exists = os.path.exists(path)
if (not exists):
  print('Web Path does not exist. Exiting');
  print('false');
else:
  path = '` + webPath + '/' + userName + `'
  exists = os.path.exists(path)
  if exists:
    print('User path alredy exists')
    shutil.rmtree('` + webPath + '/' + userName + `')
  print('Creating new path')
  os.makedirs('` + webPath + '/' + userName + `', exist_ok=True)
  try:
    copy_folder_contents('` + localPath + `', '` + webPath + '/' + userName + `')
    print('Copied!')
    print('true')
  except Exception as e:
    print('Error occurred while copying:')
    print(e)
    print('false')`;
    return code;
}
async function runCode(pythonCode) {
    console.log('Running Python code');
    console.log(pythonCode);
    console.log();
    // Ensure the session is set up before executing code
    await setupSession();
    return new Promise((resolve, reject) => {
        var _a;
        const future = (_a = session === null || session === void 0 ? void 0 : session.kernel) === null || _a === void 0 ? void 0 : _a.requestExecute({ code: pythonCode });
        if (!future) {
            reject('Failed to create kernel session.');
            return;
        }
        future.onIOPub = (msg) => {
            // Check if the message is of type 'stream' and contains 'stdout'
            console.log(msg);
            if (msg.header.msg_type === 'stream' && 'name' in msg.content && msg.content.name === 'stdout') {
                console.log('>> Stdout: ' + msg.content.text.trim() + ' <<');
                const lines = msg.content.text.trim().split('\n');
                if (lines[lines.length - 1].toLowerCase() === "true" || lines[lines.length - 1].toLowerCase() === "false") {
                    resolve(lines[lines.length - 1].toLowerCase() === "true");
                }
            }
        };
        // Ensure the session is properly shut down after execution
        future.done
            .then(() => {
            if (session) {
                console.log("Shutting down the session.");
                session.shutdown().then(() => {
                    session = null; // Reset session to allow re-setup if needed
                    console.log("Session has been shut down.");
                }).catch(shutdownError => {
                    console.error("Error during session shutdown:", shutdownError);
                });
            }
        })
            .catch((error) => {
            console.error("Error during execution:", error);
            reject(error);
        });
    });
}
async function setupSession() {
    if (session) {
        return; // If session already exists, skip re-creation
    }
    const serverSettings = _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.makeSettings();
    //const sessionManager = new SessionManager({ serverSettings });
    // Create KernelManager with server settings
    const kernelManager = new _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.KernelManager({ serverSettings });
    const sessionManager = new _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.SessionManager({ kernelManager, serverSettings });
    // Define the kernel model for the desired kernel (e.g., Python 3)
    const kernelModel = {
        name: 'python3',
        id: 'python3'
    };
    // Start a new session with a Python 3 kernel
    session = await sessionManager.startNew({
        kernel: kernelModel,
        path: '',
        type: 'file',
        name: 'PathCheckerSession'
    });
}
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugin);


/***/ })

}]);
//# sourceMappingURL=lib_index_js.241f57061c601f22ea56.js.map