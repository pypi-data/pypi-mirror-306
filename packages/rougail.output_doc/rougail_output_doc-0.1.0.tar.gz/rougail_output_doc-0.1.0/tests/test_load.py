from pytest import fixture  # , raises
from pathlib import Path
from ruamel.yaml import YAML
from rougail import RougailConfig
from rougail.output_doc import RougailOutputDoc

from .custom import CustomOption


dico_dirs = Path('../rougail/tests/dictionaries')
test_ok = set()

excludes = set([
    '60_5family_dynamic_unknown_suffix',
    '60_5family_dynamic_variable_outside_sub_suffix',
])

for test in dico_dirs.iterdir():
    if (test / 'tiramisu').is_dir() and test.name not in excludes:
        test_ok.add(test)

test_ok = list(test_ok)
test_ok.sort()

# test_ok = [dico_dirs / '60_0family_dynamic_variable_suffix']


@fixture(scope="module", params=test_ok)
def test_dir(request):
    return request.param


def _test_dictionaries(test_dir, output, namespace):
    rougailconfig = RougailConfig.copy()
    rougailconfig['step.output'] = 'doc'
    rougailconfig['doc.output_format'] = output
    rougailconfig['functions_files'] = [str(dico_dirs.parent / 'eosfunc' / 'test.py')]
#    rougailconfig['tiramisu_cache'] = "cache.py"
    dirs = [str(test_dir / 'dictionaries' / 'rougail')]
    subfolder = test_dir / 'dictionaries' / 'rougail2'
    if subfolder.is_dir():
        dirs.append(str(subfolder))
    rougailconfig['main_dictionaries'] = dirs
    if namespace:
        rougailconfig['main_namespace'] = 'Rougail'
    else:
        rougailconfig['main_namespace'] = None
    extra_dictionaries = {}
    extras = list((test_dir / 'dictionaries').iterdir())
    extras.sort()
    for extra in extras:
        if extra.name in ['rougail', 'rougail2']:
            continue
        if extra.is_dir():
            extra_dictionaries[extra.name] = [str(extra)]
    if extra_dictionaries:
        rougailconfig['extra_dictionaries'] = extra_dictionaries
    rougailconfig['custom_types']['custom'] = CustomOption
    inventory = RougailOutputDoc(rougailconfig=rougailconfig)
    doc = inventory.formater.header()
    yaml = YAML()
    len_subdir = len(str(dico_dirs)) + 1
    if extra_dictionaries:
        all_dirs = [[rougailconfig['main_dictionaries']], rougailconfig['extra_dictionaries'].values()]
    else:
        all_dirs = [[rougailconfig['main_dictionaries']]]
    for r in all_dirs:
        for dirs in r:
            for d in dirs:
                for f in Path(d).iterdir():
                    if f.name.endswith('.yml') or f.name.endswith('.yaml'):
                        doc += inventory.formater.title(str(f)[len_subdir:].split('/', 1)[-1], 1)
                        with f.open(encoding="utf8") as file_fh:
                            objects = yaml.load(file_fh)
                        doc += inventory.formater.yaml(objects)
    doc += inventory.gen_doc()
    if namespace:
        name = 'base'
    else:
        name = 'no_namespace'
    doc_file = Path('tests') / 'docs' / name / (test_dir.name + {'github': '.md', 'asciidoc': '.adoc'}.get(output))
    with doc_file.open('w') as docfh:
        docfh.write(doc)


def test_dictionaries_github(test_dir):
    _test_dictionaries(test_dir, 'github', True)


def test_dictionaries_asciidoc(test_dir):
    _test_dictionaries(test_dir, 'asciidoc', True)


def test_dictionaries_github_no_namespace(test_dir):
    if (test_dir / 'force_namespace').is_file():
        return
    _test_dictionaries(test_dir, 'github', False)


def test_dictionaries_asciidoc_no_namespace(test_dir):
    if (test_dir / 'force_namespace').is_file():
        return
    _test_dictionaries(test_dir, 'asciidoc', False)
