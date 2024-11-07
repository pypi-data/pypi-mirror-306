# -*- coding: utf-8 -*-
import subprocess
import logging
import os
import json
import sys
import zipfile
import shutil
import requests
import hashlib
import time
from datetime import datetime, timedelta
import plutonium.config as config
from uuid import uuid4
logger = logging.getLogger(__name__)
formatter = logging.Formatter(config.LOG_FORMAT)
file_handler = logging.FileHandler(config.LOG_FILENAME)
file_handler.setFormatter(formatter)
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.addHandler(console_handler)
logger.setLevel(config.LOG_LEVEL)
# 获取路径
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(__file__)
    return os.path.join(base_path, relative_path)
# 执行命令
def exec_tool(args, log_file, timeout=config.CMD_TIME_OUT, cwd=None, ):
    result = {
        'status': False,
        'message': '',
        'data': ''
    }
    try:
        logger.debug('Executing "{}"'.format(" ".join(args)))

        if os.environ.get("FETCH_LICENSE"):
            logger.debug(
                "License information would be fetched from the registry. This would take several minutes ..."
            )
        with open(log_file, 'a') as f:
            cp = subprocess.run(
                args,
                stdout=f,
                stderr=subprocess.STDOUT,
                cwd=cwd,
                env=os.environ.copy(),
                check=False,
                shell=False,
                encoding="utf-8",
                timeout=timeout
            )
            logger.debug(cp.stdout)
            result['status'] = True
    except subprocess.TimeoutExpired as timeout_error:
        logger.error(timeout)
        result['message'] = '执行超时-{}'.format(timeout_error)
    except Exception as e:
        logger.exception(e)
        result['message'] = str(e)
        return str(e)
    print(result)
    return result

def zip_folder(file_dir):
    target_file = file_dir+'/../'+file_dir.strip('/').split('/')[-1]+'.zip'
    print(target_file)
    with zipfile.ZipFile(target_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(file_dir):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, os.path.relpath(file_path, file_dir))
    

# 通过cdxgen来生成sbom
def sca_by_cdxgen(bom_file, src_dir=".", timeout=config.CMD_TIME_OUT):
    result = {
        'status': False,
        'data': {
            'cmd': '',
            'result_file': bom_file
        },
        'message': '',
    }
    cdxgen_cmd = os.environ.get("CDXGEN_CMD", "cdxgen")
    if not shutil.which(cdxgen_cmd):
        local_bin = resource_path(
            os.path.join(
                "local_bin", "cdxgen.exe" if sys.platform == "win32" else "cdxgen"
            )
        )
        if not os.path.exists(local_bin):
            result['message'] = 'command not found'
            return result
        try:
            cdxgen_cmd = local_bin
            # Set the plugins directory as an environment variable
            os.environ["CDXGEN_PLUGINS_DIR"] = resource_path("local_bin")
        except Exception as e:
            result['message'] = e
            return result
    sca_args = [cdxgen_cmd, "-o", bom_file]
    sca_args.append(src_dir)
    logger.info(sca_args)
    exec_status = exec_tool(sca_args, config.LOG_FILENAME, timeout )
    result['status'] = exec_status['status']
    result['message'] = exec_status['message']
    result['data']['cmd'] = ' '.join(sca_args)
    return result

def sca_by_opensca(bom_file, src_dir=".", log_file="",  timeout=config.CMD_TIME_OUT):
    # 获取配置文件，配置maven等信息

    result = {
        'status': False,
        'data': {
            'cmd': '',
            'result_file': bom_file
        },
        'message': '',
    }
    sca_args = ["opensca-cli", "-path", src_dir, "-config", config.TEMP_DIR+'/opensca_config.json', "-out", "{}".format(bom_file)]
    exec_status = exec_tool(sca_args, config.LOG_FILENAME, timeout)
    result['status'] = exec_status['status']
    result['message'] = exec_status['message']
    result['data']['cmd'] = ' '.join(sca_args)
    return result
def sca_by_jd_sbom_tool(bom_file, src_dir=".", log_file="",  timeout=config.CMD_TIME_OUT):
    # 获取配置文件，配置maven等信息
    result = {
        'status': False,
        'data': {
            'cmd': '',
            'result_file': bom_file
        },
        'message': '',
    }
    sca_args = ["sbom-tool", "-out ", bom_file, "-path", src_dir, "-log", log_file]
    logger.info(sca_args)
    exec_status = exec_tool(sca_args, config.LOG_FILENAME, timeout)
    result['status'] = exec_status['status']
    result['message'] = exec_status['message']
    result['data']['cmd'] = ' '.join(sca_args)
    return result

def sca_by_fosseye(bom_file, src_dir=".", log_file="",  timeout=config.CMD_TIME_OUT):
    # 获取配置文件，配置maven等信息

    result = {
        'status': False,
        'data': {
            'cmd': '',
            'result_file': bom_file
        },
        'message': '',
    }
    sca_args = ["opensca-cli", "-out ", bom_file, "-path", src_dir, "-log", log_file]
    logger.info(sca_args)
    exec_status = exec_tool(sca_args, config.LOG_FILENAME, timeout)
    result['status'] = exec_status['status']
    result['message'] = exec_status['message']
    result['data']['cmd'] = ' '.join(sca_args)
    return result

def sca_by_syft(bom_file, src_dir=".", log_file="",  timeout=config.CMD_TIME_OUT):
    result = {
        'status': False,
        'data': {
            'cmd': '',
            'result_file': bom_file
        },
        'message': '',
    }
    sca_args = ["syft", src_dir, "-o", "syft-json={}".format(bom_file)]
    exec_status = exec_tool(sca_args, config.LOG_FILENAME, timeout)
    result['status'] = exec_status['status']
    result['message'] = exec_status['message']
    result['data']['cmd'] = ' '.join(sca_args)
    return result

def vul_by_grype(result_file, src_dir=".", log_file="", sbom_file="", timeout=config.CMD_TIME_OUT):
    result = {
        'status': False,
        'data': {
            'cmd': '',
            'result_file': bom_file
        },
        'message': '',
    }
    if sbom_file:
        vul_args = ["grype", "sbom:{}".format(sbom_file), "-o", "json", "--file", "{}".format(result_file)]
    else:
        vul_args = ["grype", "dir:{}".format(src_dir), "-o", "json", "--file", "{}".format(result_file)]
    exec_status = exec_tool(vul_args, config.LOG_FILENAME, timeout)
    result['status'] = exec_status['status']
    result['message'] = exec_status['message']
    result['data']['cmd'] = ' '.join(vul_args)
    return result

def vul_by_trivy():
    pass

def vul_by_depscan():
    pass

class ImageFileExtractor(object):
    def __init__(self, tmp_dir='./tmp/', result_dir='./'):
        self.tmp_dir = tmp_dir
        self.result_dir = result_dir

    def calculate_md5(self, file_path):
        md5_hash = hashlib.md5()
        with open(file_path, "rb") as f:
            # Read and update hash string value in blocks of 4K
            for byte_block in iter(lambda: f.read(4096), b""):
                md5_hash.update(byte_block)
        return md5_hash.hexdigest()

    def calculate_sha256(self, file_path):
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            # Read and update hash string value in blocks of 4K
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()

    # 从分层解压目录中获取可执行文件
    def get_executable_files(self, base_folder, layer_id, layer_diff_id):
        logger.info('开始获取可执行文件')
        result_list = []
        for root, dirs, files in os.walk(base_folder):
            for filename in files:
                file_path = os.path.join(root, filename)
                # Check if the file is executable
                if os.access(file_path, os.X_OK):
                    sha256 = self.calculate_sha256(file_path)
                    file_md5 = self.calculate_md5(file_path)
                    file_path = file_path.replace(base_folder, '')
                    try:
                        result_list.append({
                            "filename": filename,
                            "file_path": file_path,
                            "md5": file_md5,
                            "sha256": sha256,
                            "layer_id": layer_id,
                            "layer_diff_id": layer_diff_id,
                            # "unique_hash": md5((filename + file_path + file_md5).encode()).hexdigest()
                        })
                        # unique hash
                    except Exception as e:
                        logger.error(e)
        return result_list

    def run_command(self, command):
        return os.popen(command).read()

    # 解压镜像，并获取可执行文件数据
    def get_execute_file_data_from_image(self, image_info, image_file, result_file):
        result = {
            'status': False,
            'message': '',
            'data': {
                'data': None,
                'file_url': '',
                'file_url_oss': '',
            }
        }
        all_data = {
            'image_full_name': image_info.get('image_full_name'),
            'image_name': image_info.get('image_name'),
            'image_tag': image_info.get('image_tag'),
            'image_id': image_info.get('image_id'),
            'image_unique_hash': image_info.get('unique_hash'),
            'layer_data': {},
            'execute_files': []
        }
        
        image_extract_dir = self.tmp_dir + uuid4().hex
        logger.info('镜像解压存储目录为-{}'.format(image_extract_dir))
        if not os.path.exists(image_extract_dir):
            os.makedirs(image_extract_dir)
        layer_extract_dir = self.tmp_dir + uuid4().hex
        # layer_extract_dir = './tmp/26f0a52d1d8d4fa19bad3f4865f94b88'
        logger.info('镜像分层解压存储目录为-{}'.format(layer_extract_dir))
        if not os.path.exists(layer_extract_dir):
            os.makedirs(layer_extract_dir)
        logger.info('开始解压镜像文件')
        extract_image_command = 'tar -xf {} --directory {}'.format(image_file, image_extract_dir)
        os.system(extract_image_command)
        logger.info('完成解压镜像文件')
        # 删除镜像文件
        logger.info('开始删除镜像tar文件')
        try:
            image_tar_dir = '/'.join(image_file.split('/')[:-1])
            if image_tar_dir.startswith('/data/voyager_sbom/data/'):
                shutil.rmtree(image_tar_dir)
        except Exception as e:
            logger.error(e)

        # docker inspect数据为diff id
        # 镜像解压后的目录名为layer id，里面的layer.tar计算sha256即为diff id
        image_data = None
        try:
            with open(image_extract_dir + '/manifest.json', 'r') as f:
                image_data = json.loads(f.read())
        except Exception as e:
            logger.error(e)
        layer_data = {}
        layer_file_map = {}
        # key为diff id(layer id sha256)
        # 值为layer id
        if image_data and len(image_data) > 1:
            logger.info("镜像manifest数据大于一个，需排查")
        try:
            for layer in image_data[0].get('Layers'):
                # 有的Layers的结尾是layer_id+'.tar'
                # 数据中有如下几种格式
                # d0241a0d0759b0d4adbfc4d9278479e28d4762abaaa21ba4135fc58710dbd88d/layer.tar格式
                # 0ad3ddf4a4ce0fc9d65021897541c99e5497a11ced2419016147267df61732d3.tar
                # "blobs/sha256/8a99c598a0e4dd63ed2ab07cb5ba08b51988ba78dd022c4c28a24ed40f91de5a
                if sys.platform == 'darwin':
                    output = self.run_command("ls {}/{} | xargs shasum -a 256".format(image_extract_dir, layer))
                else:
                    output = self.run_command("ls {}/{}| xargs sha256sum".format(image_extract_dir, layer))
                diff_id = output.split()[0].strip()

                # oci镜像
                if layer.startswith('blobs/sha256'):
                    layer_id = layer.split('/')[-1]
                else:
                    if layer.endswith('/layer.tar'):
                        layer_id = layer.split('/')[0]
                    else:
                        layer_id = layer.split('.')[0]
                layer_file_map[diff_id] = layer
                layer_data[diff_id] = layer_id
        except Exception as e:
            logger.error(e)
        # 分层数据
        all_data['layer_data'] = layer_data
        logger.info('分层数据为[diff id] -> [layer id]')
        logger.info('开始解压分层文件')
        all_file_data = {}
        for diff_id in layer_data:
            # 创建新的目录，目录为diff id，里面存储解压文件内容
            layer_item_dir = layer_extract_dir + '/' + layer_data[diff_id]
            if not os.path.exists(layer_item_dir):
                os.makedirs(layer_item_dir)
            # os.system(f"mkdir -p {dest}")
            logger.info('开始解压分层-diff id is {}'.format(diff_id))
            logger.info('开始解压分层layer id为-{}，diff id为-{}'.format(layer_data[diff_id], diff_id))
            os.system("tar -xf {}/{} --directory {}".format(image_extract_dir, layer_file_map[diff_id], layer_item_dir))
            logger.info("tar -xf {}/{} --directory {}".format(image_extract_dir, layer_file_map[diff_id], layer_item_dir))
            # 遍历全部文件内容，获取可执行文件、路径、sha256
            execute_files = self.get_executable_files(layer_item_dir, layer_data[diff_id], diff_id)
            all_file_data[diff_id] = execute_files
        logger.info("完成分析")
        all_data['execute_files'] = all_file_data
        # 写入数据到文件
        # 清理解压
        try:
            shutil.rmtree(image_extract_dir)
            shutil.rmtree(layer_extract_dir)
        except Exception as e:
            logger.error(e)
        # 写入数据到文件
        try:
            with open(result_file, 'w') as f:
                f.write(json.dumps(all_data))
                result['status'] = True
                result['data']['data'] = all_data
                result['data']['file_url'] = result_file
        except Exception as e:
            logger.error(e)
            result['message'] = str(e)

        return result


# 执行对镜像的分析，并输出结果文件


# 服务端检测
class VoyagerDetect():
    def __init__(self, token=None, url=None, username=None, password=None, api=None):
        self.api_url = url
        self.api_token = token
        self.api_username = username
        self.api_password = password
        self.req = requests.Session()
        self.error_try_count = 5
        self.req_time_out = 60
        self.time_wait_for_report = 10
        self.cmd_time_out = 10
    def set_req_time_out(self, time_seconds):
        self.req_time_out = time_seconds
    def set_error_try_count(self, count):
        self.error_try_count = count

    def set_time_wait_for_report(self, time_seconds):
        self.time_wait_for_report = time_seconds
    def set_cmd_time_out(self,time_seconds):
        self.cmd_time_out = time_seconds
        

    # 1.token生成，token有效期较长，失效后再进行重新生成
    def get_new_token(self):
        try:
            self.req.headers = {}
            res = self.req.post(self.api_url + config.VOYAGER_GET_TOKEN_API,
                                data={'username': self.api_username, 'password': self.api_password},)
            token = res.json()['token']
            headers = {
                # 注意Token后有空格
                'Authorization': 'Token ' + token
            }
            self.req.headers = headers
            return token
        except Exception as e:
            logger.error(e)
            return None

    def check_token_valid(self):
        headers = {
            # 注意Token后有空格
            'Authorization': 'Token ' + self.api_token
        }
        self.req.headers = headers
        try:
            res = self.req.get(self.api_url + config.VOYAGER_CHECK_TOKEN_API)
            if res.status_code == 200 and res.json()['success']:
                logger.info('token有效')
                return True
            else:
                logger.error('token无效')
                logger.info(res.text)
        except Exception as e:
            logger.info('token失效')
            logger.error(e)
        return False
    # 登录认证
    def login(self):
        login_status = {
            'status': False,
            'message': '',
            'data': None
        }
        if self.api_token:
            if self.check_token_valid():
                login_status['status'] = True
                return login_status
            else:
                # token失效，使用账号密码登录
                login_status['message'] = 'token失效，使用账号密码登录'

        if self.api_username and self.api_password:
            # 获取认证token
            token = self.get_new_token()
            # logger.info(token)
            if token:
                self.api_token = token
                headers = {
                    # 注意Token后有空格
                    'Authorization': 'Token ' + self.api_token
                }
                self.req.headers = headers
                login_status['status'] = True
            else:
                login_status['message'] = '无法生成访问token，账号密码可能错误'
        else:
            login_status['message'] = '请提供API账号以及密码信息'
        logger.info(login_status['message'])
        return login_status

    def init_opensca(self):
        login_status = self.login()
        data = {
            'type': 'get_opensca_config',
        }
        if login_status['status']:
            response = self.req.post(self.api_url + config.VOYAGER_BASE_API, data=data,
                                         files=[('files', ('', None,)), ])
            try:
                print(response.json())
                if response.json().get('success'):
                    config_data = response.json().get('data')
                    print(config.TEMP_DIR+'opensca_config.json')
                    with open(config.TEMP_DIR+'/opensca_config.json', 'w') as f:
                        f.write(json.dumps(config_data))
            except Exception as e:
                logger.error(e)
        else:
            return login_status['message']

    # sca分析
    def sca_analysis(self, src_dir=".", tool='cdxgen'):
        if tool == 'cdxgen':
            result_file = config.DATA_DIR+'/{}_{}.json'.format(tool, uuid4().hex)
            return sca_by_cdxgen(result_file, src_dir)
        elif tool == 'opensca':
            self.init_opensca()
            result_file = config.DATA_DIR+'/{}_{}.json'.format(tool, uuid4().hex)
            log_file = config.DATA_DIR+'/{}_log_{}.log'.format(tool, uuid4().hex)
            return sca_by_opensca(result_file, src_dir, log_file)
        elif tool == 'syft':
            result_file = config.DATA_DIR + '/{}_{}.json'.format(tool, uuid4().hex)
            log_file = config.DATA_DIR + '/{}_log_{}.log'.format(tool, uuid4().hex)
            return sca_by_syft(result_file, src_dir, log_file)
        elif tool == 'grype':
            result_file = config.DATA_DIR + '/{}_{}.json'.format(tool, uuid4().hex)
            log_file = config.DATA_DIR + '/{}_log_{}.log'.format(tool, uuid4().hex)
            sbom_result_file = None
            try:
                for i in os.listdir(config.DATA_DIR):
                    if i.startswith('syft_'):
                        sbom_result_file = config.DATA_DIR + '/' + i
                        break
            except Exception as e:
                logger.error(e)
            return vul_by_grype(result_file, src_dir, log_file, sbom_result_file)
        elif tool == 'jd-sbom-tool':
            pass

        return None

    # 上传文件获得文件id
    def upload_files(self,files):
        data = {
            'type': 'file'
        }
        login_status = self.login()
        if login_status['status']:
            try:
                response = self.req.post(self.api_url + config.VOYAGER_UPLOAD_API, data=data, files=files, timeout=self.req_time_out)
                return response.json()
            except Exception as e:
                logger.error(e)
                return None
        else:
            return login_status['message']
    # upload
    def upload(self, data, files):
        login_status = self.login()
        if login_status['status']:
            try:
                if files:
                    response = self.req.post(self.api_url + config.VOYAGER_BASE_API, data=data, files=files, timeout=self.req_time_out)
                else:
                    response = self.req.post(self.api_url + config.VOYAGER_BASE_API, data=data,
                                             files=[('files', ('', None,)), ], timeout=self.req_time_out)
                return response.json()
            except Exception as e:
                logger.error(e)
        else:
            return login_status['message']

    # 获取扫描结果或报告
    def get_scan_result(self, task_id):
        login_status = self.login()
        if login_status['status']:
            try:
                response = self.req.get(self.api_url + config.VOYAGER_BASE_API+'?task_id={}'.format(task_id),)
                return response.json()
            except Exception as e:
                logger.error(e)
                return None
        else:
            return login_status
    def get_detect_result(self, task_id):
        login_status = self.login()
        if login_status['status']:
            try:
                response = self.req.get(self.api_url + config.VOYAGER_DETECT_API+'?task_id={}'.format(task_id),)
                return response.json()
            except Exception as e:
                logger.error(e)
                return None
        else:
            return login_status
    # 根据镜像名、镜像文件在服务端进行镜像漏洞检测
    def scan_image_in_server(self, data, files):
        login_status = self.login()
        if login_status['status']:
            if files:
                response = self.req.post(self.api_url + config.VOYAGER_DETECT_API, data=data, files=files)
            else:
                response = self.req.post(self.api_url + config.VOYAGER_DETECT_API, data=data, files=[('files', ('', None,)), ])
            return response.json()
        else:
            return login_status['message']

    def image_analysis(self, src_dir='.', tool='custom', analysis_type='sca', image_info={}, image_file=None, sca_result_file=None,
                       dockerfile_path=None):
        result = {
            'status': False,
            'data': {
                'cmd': '',
                'result_file': ''
            },
            'message': '',
        }
        op_msg = ''
        cmd_args = []
        result_file = config.DATA_DIR+'/{}--{}--result.json'.format(analysis_type, tool)
        # 镜像文件
        if not image_file:
            image_file = src_dir + '/' + 'image.tar'

        if analysis_type == 'sca':
            if tool == 'syft':
                op_msg = '基于syft进行镜像的SCA分析'
                cmd_args = ["syft", image_file, "-o", "syft-json={}".format(result_file)]
            elif tool == 'trivy':
                op_msg = '基于trivy进行镜像的SCA分析'
                # trivy image --format cyclonedx --output /tmp/sca_trivy_result.json --input /tmp/hi.tar
                cmd_args = ["trivy", "image", "--format", "cyclonedx", "--output", result_file, "--input", image_file]
            else:
                pass
        elif analysis_type == 'vul_by_sbom':
            if tool == 'grype':
                op_msg = '基于grype进行镜像的漏洞分析'
                sca_file = result_file.format('sca', 'syft')
                cmd_args = ["grype", "sbom:{}".format(sca_file), "-o", "json", "--file", result_file]

            elif tool == 'trivy':
                op_msg = '基于trivy进行镜像的漏洞分析'
                sca_file = result_file.format('sca', 'trivy')
                cmd_args = ["trivy", "--scanners", "vuln,misconfig,secret", "sbom", sca_file, "--format json", "-o",
                            result_file]
            else:
                pass
        elif analysis_type == 'vul':
            if tool == 'grype':
                op_msg = '基于grype进行镜像的漏洞分析'
                cmd_args = ["grype", image_file, "-o", "json", "--file", result_file]

            elif tool == 'trivy':
                op_msg = '基于trivy进行镜像的漏洞分析'
                cmd_args = ["trivy", "image", "--scanners", "vuln,misconfig,secret", "--format json", "-o", result_file,
                            "--input",
                            image_file]
            else:
                pass
        elif analysis_type == 'exec':
            image_extractor = ImageFileExtractor()
            op_msg = '镜像可执行文件分析提取'
            logger.info('[开始]' + op_msg)
            exec_files_result = image_extractor.get_execute_file_data_from_image(image_info, image_file, result_file)
            if exec_files_result['status']:
                result['status'] = True
                logger.info('[完成]' + op_msg)
            else:
                logger.info('[异常]' + op_msg)
                logger.info(exec_files_result['message'])
                result['message'] = exec_files_result['message']
        elif analysis_type == 'backdoor':
            pass
        elif analysis_type == 'dockerfile':
            op_msg = '读取Dockerfile文件内容'
            logger.info('[开始]' + op_msg)
            # 读取该文件，并写入结果文件
            if not dockerfile_path:
                dockerfile_path = src_dir + '/' + 'Dockerfile'
            if not os.path.exists(dockerfile_path):
                result['message'] = '不存在Dockerfile文件'
                logger.info('[异常]' + op_msg)
            try:
                with open(dockerfile_path, 'r') as f:
                    data = f.read()
                    with open(result_file, 'w') as w:
                        w.write(data)
                        logger.info('[完成]' + op_msg)
                        result['status'] = True
            except Exception as e:
                logger.error(e)
                logger.info('[异常]' + op_msg)
                result['message'] = str(e)
        else:
            logger.info('分析类型待扩展')
        logger.info('[开始]' + op_msg)
        logger.info(cmd_args)
        if len(cmd_args) >0:
            exec_status = exec_tool(cmd_args, config.LOG_FILENAME, self.cmd_time_out)
            if exec_status['status']:
                logger.info('[完成]' + op_msg)
            else:
                logger.info('[异常]' + op_msg)
                logger.info(exec_status['message'])
        result['data']['cmd'] = ' '.join(cmd_args)
        result['data']['result_file'] = result_file
        return result

    def make_detect_req(self, data):
        login_status = self.login()
        if login_status['status']:
            try:
                res = self.req.post(self.api_url+config.VOYAGER_DETECT_API, data=data,)
                return res.json()
            except Exception as e:
                logger.error(e)
                return None
        else:
            return login_status['message']

    # 添加超时时间，命令执行超时时间、检测耗时超时时间
    def detect(self, data,):
        # 默认安全检测为通过，即安全服务异常情况下其允许通过
        result = {
            'passed': True,
            'message': '',
            'data': None
        }
        scan_status = self.make_detect_req(data)
        try_count = 1
        while try_count <= self.error_try_count:
            if scan_status:
                if scan_status['success']:
                    task_id = scan_status['data']
                    scan_run_time = datetime.now()
                    # 轮询获取扫描结果，直到任务完成或超时时间超过5分钟
                    while True:
                        scan_result = self.get_detect_result(task_id)
                        logger.info(scan_result)
                        if scan_result:
                            try:
                                # 代表任务执行完成
                                if scan_result['data']['status'] in ['success', 'error']:
                                    result['passed'] = scan_result['data']['passed']
                                    result['message'] = scan_result['data']['message']
                                    result['data'] = scan_result['data']['data']
                                    break
                                else:
                                    logger.info('任务正在执行，等待尝试继续查询')
                                    time.sleep(10)
                            except Exception as e:
                                logger.error(e)
                                time.sleep(10)
                        else:
                            logger.info('调用查看检测结果服务异常，等待尝试基线查询')
                            time.sleep(10)

                        if datetime.now() > scan_run_time + timedelta(seconds=int(self.time_wait_for_report)):
                            logger.info('等待超时，结束服务调用')
                            break
                    break
                else:
                    logger.info('调用扫描服务失败-{}'.format(scan_status['message']))
                    try_count += 1
                    time.sleep(10)
            else:
                try_count += 1
                logger.info('调用扫描服务请求异常，正在重新尝试第{}次'.format(try_count))
                time.sleep(10)
                scan_status = self.make_detect_req(data)
        if result['passed']:
            logger.info('当前镜像检测通过，可以继续执行流水线')
            logger.info(result['message'])
        else:
            logger.info('当前镜像检测未通过，流水线终止执行，可查看相关加白申请')
            logger.info(result['message'])
            logger.info(result['data'])
        return result

    # 镜像可执行文件提取
    # 镜像sca分析，使用syft/trivy并将结果上传
    # 镜像sca分析以及漏洞检测，并将结果上传
    