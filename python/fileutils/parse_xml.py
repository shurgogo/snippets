import os
import sys
import xml.etree.cElementTree as et


def read_xml(file_path):
    tree = et.parse(os.path.join(file_path, 'my.xml'))
    root = tree.getroot()
    product = {
        'type': root.get('type'),
        'version': root.get('version'),
        'base_version': root.get('base_version'),
        'business_version': root.get('business_version')
    }

    base_images = []
    for base_image in root.find('base-images').findall('base-image'):
        base_image = {
            'name': base_image.get('name'),
            'version': base_image.get('version')
        }
        base_images.append(base_image)

    return product, base_images


if __name__ == '__main__':
    xml_file_path = sys.argv[1]
    try:
        value = read_xml(xml_file_path)
        print(value)
    except Exception as e:
        print('parse error: ', e)
