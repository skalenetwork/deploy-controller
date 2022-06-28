import json
from os.path import normpath, join, dirname

name = 'ConfigController'
artifacts_path = normpath(join(dirname(__file__), '../../artifacts/'))
package_artifacts_path = normpath(join(dirname(__file__), '../config_controller_predeployed/artifacts'))


def get_build_info_path():
    dbg_path = join(artifacts_path, 'contracts', f'{name}.sol')
    with open(join(dbg_path, f'{name}.dbg.json')) as dbg_file:
        dbg = json.loads(dbg_file.read())
        return normpath(join(dbg_path, dbg['buildInfo']))


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


if __name__ == '__main__':
    main()
