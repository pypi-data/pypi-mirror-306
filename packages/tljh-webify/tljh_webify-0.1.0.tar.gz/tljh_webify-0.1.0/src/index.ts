import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';
import { ICommandPalette } from '@jupyterlab/apputils';
import { Kernel, KernelManager, ServerConnection, SessionManager, KernelMessage, Session } from '@jupyterlab/services';
import { IFileBrowserFactory } from '@jupyterlab/filebrowser';

/**
 * Initialization data for the webify extension.
 */
const webPath = '/mnt/tljhweb';
const URL = 'https://tljhweb.ictsoeasy.co.uk';
let session: Session.ISessionConnection | null = null; // Global session variable

const webify_command = 'webify:webify';
const plugin: JupyterFrontEndPlugin<void> = {
  id: 'webify:plugin',
  description: 'A JupyterLab extension to copy files from a jupyter lab user folder to a different folder (to be served on a web)',
  autoStart: true,
  requires: [ICommandPalette, IFileBrowserFactory],
  activate: (app: JupyterFrontEnd, palette: ICommandPalette, fileBrowserFactory: IFileBrowserFactory) => {
    console.log('JupyterLab extension webify is activated!');
    const { tracker } = fileBrowserFactory;
    app.commands.addCommand(webify_command, {
      label: 'Webify',
      caption: 'Webify',
      execute: async (args: any) => {
        //console.log('Args:'+args);
        const widget = tracker.currentWidget;
        if (!widget) {
          console.log('No widget');
          return;
        }
        const path = widget.selectedItems().next();
        //console.log(JSON.stringify(path, null, 2));
        console.log('We are going to move:'+path.value.path);
        const localPath = path.value.path;
        moveFilesForWebify(localPath);
      }
    });

    const category = 'WHO';
    palette.addItem({ command: webify_command, category, args: { origin: 'from palette'} });
    
    // Add the command to the file browser context menu, limited to directories
    app.contextMenu.addItem({
      command: webify_command,
      selector: '.jp-DirListing-item[data-isdir="true"]', // Ensures it only appears for folders
      rank: 10
    });


  }
};

async function moveFilesForWebify(localPath: string) {
  // Identify student's name
  const currentURL = window.location.href;
  console.log("Current URL:", currentURL);
  const urlParts = window.location.pathname.split('/');
  const userIndex = urlParts.indexOf('user');
  const username = userIndex !== -1 ? urlParts[userIndex + 1] : "Unknown User";
  console.log("Current Username:", username);
  const codeRun = await runCode(generatePythonCode(webPath,username,localPath))
    .catch(error => {
      console.log('Error running code:',error);
    })
  console.log('Code run:'+codeRun);
  console.log('All finished');
  window.open(URL+'/'+username, '_blank');
}

function generatePythonCode(webPath: string, userName: string, localPath: string): string {
  var code = `import os
import shutil
path = '`+webPath+`'
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
  path = '`+webPath+'/'+userName+`'
  exists = os.path.exists(path)
  if exists:
    print('User path alredy exists')
    shutil.rmtree('`+webPath+'/'+userName+`')
  print('Creating new path')
  os.makedirs('`+webPath+'/'+userName+`', exist_ok=True)
  try:
    copy_folder_contents('`+localPath+`', '`+webPath+'/'+userName+`')
    print('Copied!')
    print('true')
  except Exception as e:
    print('Error occurred while copying:')
    print(e)
    print('false')`;
  return code;
}

/**
 * Function to check if a file system path exists using a temporary Python kernel.
 */
async function runCode(pythonCode: string): Promise<boolean> {
  console.log('Running Python code');
  console.log(pythonCode);
  console.log();

  // Ensure the session is set up before executing code
  await setupSession();

  return new Promise((resolve, reject) => {
      const future = session?.kernel?.requestExecute({ code: pythonCode });

      if (!future) {
          reject('Failed to create kernel session.');
          return;
      }

      future.onIOPub = (msg: KernelMessage.IMessage) => {
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

async function setupSession(): Promise<void> {
  if (session) {
      return; // If session already exists, skip re-creation
  }

  const serverSettings = ServerConnection.makeSettings();
  //const sessionManager = new SessionManager({ serverSettings });
  // Create KernelManager with server settings
  const kernelManager = new KernelManager({ serverSettings });
  const sessionManager = new SessionManager({ kernelManager, serverSettings });

  // Define the kernel model for the desired kernel (e.g., Python 3)
  const kernelModel: Kernel.IModel = {
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

export default plugin;
