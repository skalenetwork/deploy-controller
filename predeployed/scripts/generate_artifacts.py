import json
import shutil
from os.path import normpath, join, dirname

name = 'ConfigController'
pkg_name = 'config_controller_predeployed'

artifacts_dir = normpath(join(dirname(__file__), '../../artifacts/', 'contracts', f'{name}.sol'))
package_artifacts_path = normpath(join(dirname(__file__), f'../{pkg_name}/artifacts'))


def get_build_info_path():
    with open(join(artifacts_dir, f'{name}.dbg.json')) as dbg_file:
        dbg = json.loads(dbg_file.read())
        return normpath(join(artifacts_dir, dbg['buildInfo']))


def main():
    build_info_path = get_build_info_path()
    with open(build_info_path) as info_file:
        info = json.loads(info_file.read())
        meta_data = {
            'name': name,
            'solcVersion': info['solcVersion'],
            'solcLongVersion': info['solcLongVersion'],
            'input': info['input']
        }
    with open(join(package_artifacts_path, f'{name}.meta.json'), 'w') as meta:
        meta.write(json.dumps(meta_data, indent=4))
    shutil.copy(join(artifacts_dir, f'{name}.json'), package_artifacts_path)


if __name__ == '__main__':
    main()
