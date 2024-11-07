# -*- coding: utf-8 -*-
import json
import os
import argparse
from hashlib import md5
from plutonium.utils import logger, VoyagerDetect, zip_folder
from plutonium.config import (
    VOYAGER_SERVER,
    VOYAGER_USERNAME,
    VOYAGER_PASSWORD,
    VOYAGER_TOKEN,
    LOG_FILENAME,
    LOGO,
    DATA_DIR,
    AGENT_UUID
)
def init_parse():
    parser = argparse.ArgumentParser(
        description="SCA Agent based on Cdxgen and internal project Voyager I, for application dependencies and risk discovery。"
    )
    parser.add_argument(
        "-t",
        "--type",
        dest="type",
        required=True,
        help="project_sca/image_sca/package_sca/api/other/project_vul/image_vul/image_exec/image_detect",
    )
    # project_sca
    # image_sca
    # image_detect
    parser.add_argument(
        "-trigger-source",
        "--trigger-source",
        dest="trigger_source",
        help="Trigger Source",
    )
    parser.add_argument(
        "--scene-token",
        dest="scene_token",
        help="Scene token",
    )
    parser.add_argument(
        "-s",
        "--source",
        dest="source",
        required=True,
        help="Source directory or container image or binary file",
    )
    parser.add_argument(
        "--tool",
        dest="tool",
        help="Analysis Tool",
    )
    parser.add_argument(
        "--tool-opitons",
        dest="tool_options",
        help="Analysis Tool options",
    )
    parser.add_argument(
        "--firewall-status",
        dest="firewall_status",
        action="store_true",
        default=False,
        help="是否进行拦截检测",
    )
    parser.add_argument(
        "--is-sync",
        dest="is_sync",
        action="store_true",
        default=False,
        help="是否同步检测",
    )
    # 服务端参数
    parser.add_argument(
        "--voyager-server",
        default=VOYAGER_SERVER,
        dest="voyager_server",
        help="Voyager server url. Eg: https://api.voyager.com",
    )
    parser.add_argument(
        "--voyager-username",
        default=VOYAGER_USERNAME,
        dest="voyager_username",
        help="Voyager username",
    )
    parser.add_argument(
        "--voyager-password",
        default=VOYAGER_PASSWORD,
        dest="voyager_password",
        help="Voyager password",
    )
    parser.add_argument(
        "--voyager-token",
        default=VOYAGER_TOKEN,
        dest="voyager_token",
        help="Voyager token for token based submission",
    )
    parser.add_argument(
        "--voyager-api",
        default="",
        dest="voyager_api",
        help="Voyager api url",
    )
    parser.add_argument(
        "--analyze-uuid",
        dest="analyze_uuid",
        help="分析任务id",
    )
    # 项目参数信息
    parser.add_argument(
        "--project-name",
        dest="project_name",
        help="project name",
    )
    parser.add_argument(
        "--project-url",
        dest="project_url",
        help="project repository url",
    )
    parser.add_argument(
        "--project-user",
        dest="project_user",
        help="project user",
    )
    parser.add_argument(
        "--user-email",
        dest="user_email",
        help="操作用户邮箱",
    )
    parser.add_argument(
        "--project-branch",
        dest="project_branch",
        help="project branch",
    )
    parser.add_argument(
        "--project-file",
        dest="project_file",
        help="project file",
    )
    parser.add_argument(
        "--project-commit-id",
        dest="project_commit_id",
        help="project commit id",
    )
    #
    parser.add_argument(
        "--image-data-type",
        dest="image_data_type",
        help="镜像数据类型，image_name/image_file/image_dockerfile/image_analysis_file",
    )
    parser.add_argument(
        "--image-analysis-file",
        dest="image_analysis_file",
        help="镜像分析结果文件",
    )
    parser.add_argument(
        "--image-analysis-file-type-list",
        dest="image_analysis_file_type_list",
        help="镜像分析结果文件类型列表dockerfile--custom,sca--trivy,sca--syft,exec--custom,vul--trivy,vul--grype",
    )
    # 镜像参数信息
    parser.add_argument(
        "--image-name",
        dest="image_name",
        help="镜像名称",
    )
    parser.add_argument(
        "--image-full-name",
        dest="image_full_name",
        help="镜像完整名称",
    )
    parser.add_argument(
        "--image-id",
        dest="image_id",
        help="镜像Id",
    )
    parser.add_argument(
        "--image-type",
        dest="image_type",
        help="镜像类型,name/file/dockerfile",
    )
    parser.add_argument(
        "--image-file",
        dest="image_file",
        help="镜像文件",
    )
    parser.add_argument(
        "--image-sca-file",
        dest="image_sca_file",
        help="镜像SCA结果文件",
    )
    parser.add_argument(
        "--dockerfile-path",
        dest="dockerfile_path",
        help="dockerfile路径",
    )
    parser.add_argument(
        "--scan-in-server",
        dest="scan_in_server",
        action="store_true",
        default=False,
        help="是否在服务端扫描",
    )
    parser.add_argument(
        "--image-analysis-type",
        dest="image_analysis_type",
        help="sca/exec/vul/sca_vul/backdoor/other",
    )
    parser.add_argument(
        "--image-repository-url",
        dest="image_repository_url",
        help="镜像仓库地址",
    )
    parser.add_argument(
        "--extra-data",
        dest="extra_data",
        help="附加参数a=b&c=d",
    )
    parser.add_argument(
        "--error-try-count",
        dest="error_try_count",
        default=5,
        help="错误尝试次数",
    )
    parser.add_argument(
        "--cmd-time-out",
        dest="cmd_time_out",
        default=30,
        help="命令执行超时时间",
    )
    parser.add_argument(
        "--time-wait-for-report",
        dest="time_wait_for_report",
        default=20,
        help="等待检测报告时间",
    )
    # parser.print_help()
    return parser.parse_args()


def main():
    # print(LOGO)
    args = init_parse()
    data = {
        'type': args.type,
        'agent_uuid': AGENT_UUID,
        'trigger_source': args.trigger_source,
        'scene': args.scene_token,
        'tool': args.tool,
        'tool_options': args.tool_options,
        'firewall_status': args.firewall_status,
        'is_sync': args.is_sync,
        'analyze_uuid': args.analyze_uuid if args.analyze_uuid else '',
        # 项目信息
        # 镜像类
        'image_name': args.image_name,
        'image_full_name': args.image_full_name,
        'image_repository_url': args.image_repository_url,
        'image_analysis_type': args.image_analysis_type,
        'image_data_type': args.image_data_type,
        'image_type': args.image_type,
        'image_analysis_file': args.image_analysis_file,
        'image_analysis_file_type_list': args.image_analysis_file_type_list,
        # 项目类
        'project_name': args.project_name,
        'project_branch': args.project_branch,
        'project_user': args.project_user,
        'user_email': args.user_email,
        'project_commit_id': args.project_commit_id,
        'project_url': args.project_url,
        # 附加参数
        'extra_data': args.extra_data,
    }
    if not data['image_name']:
        if data.get('image_full_name'):
            data['image_name'] = data.get('image_full_name', '').split(':')[0]
    attach_files = [
        # 提交的名称前缀需要与scan_log_detail的type一致
        # 项目文件
        # ('log_file', (SCA, open('./todo.md', 'rb'),)),
        # ('core_files_list', ('pom.xml', open('./todo.md', 'rb'), )),
        # ('core_files_list', ('package.json.lock', open('./todo.md', 'rb'), )),
        # ('sbom_files_list', ('sca_cdxgen.json', open('./voyager.json', 'rb'),)),
        # ('sbom_files_list', ('sca_dependency_tree.txt', open('./todo.md', 'rb'), )),
        # ('vul_files_list', ('vul_veinmind.json', open('./todo.md', 'rb'), )),
    ]
    detector = VoyagerDetect(
        token=args.voyager_token if args.voyager_token else VOYAGER_TOKEN,
        url=args.voyager_server if args.voyager_server else VOYAGER_SERVER,
        username=args.voyager_username if args.voyager_username else VOYAGER_USERNAME,
        password=args.voyager_password if args.voyager_password else VOYAGER_PASSWORD,
        api=args.voyager_api if args.voyager_api else ''
    )
    if args.time_wait_for_report:
        detector.set_time_wait_for_report(args.time_wait_for_report)
    if args.error_try_count:
        detector.set_error_try_count(args.error_try_count)
    if args.cmd_time_out:
        detector.set_cmd_time_out(int(args.cmd_time_out))

    # 项目安全检测
    if args.type in ['project_sca']:
        # 逐步进行检测
        for tool in args.tool.split(','):
            detector.sca_analysis(args.source, tool)
        # 打包上传
        zip_folder(DATA_DIR)
        target_file = DATA_DIR.rstrip('/')+'.zip'
        try:
            attach_files.append(
                ('files', (target_file.split('/')[-1], open(target_file, 'rb'),)),
            )
        except Exception as e:
            logger.error(e)
        scan_status = detector.upload(data, attach_files)
        print(scan_status)
    # 服务端执行镜像SCA分析、执行镜像漏洞检测，并获得检测结果
    # image_vul_detect会进行结果的规则检测，返回是否命中，image_sca_detect会对结果文件进行规则检测，返回是否命中
    elif args.type in ['image_vul', 'image_sca', 'image_vul_detect', 'image_sca_detect']:
        image_info = {
            'image_name': args.image_name,
            'image_full_name': args.image_full_name,
            'image_tag': None,
            'image_id': args.image_id,
            'unique_hash': None
        }
        try:
            image_tag = args.image_full_name.split(':')[-1]
            image_tag = args.image_full_name.split(':')[-1]
            image_unique_hash = md5((args.trigger_source + args.image_full_name).encode()).hexdigest()
            image_info['image_tag'] = image_tag
            image_info['unique_hash'] = image_unique_hash
        except Exception as e:
            logger.error(e)
        if args.scan_in_server:
            logger.info('在服务端执行相应的分析操作')
            # image_file/image_dockerfile/image_analysis_file
            if args.image_data_type in ['image_file', 'image_dockerfile', 'image_analysis_file']:
                file_info = None
                if args.image_data_type == 'image_file':
                    file_info = args.image_file
                elif args.image_data_type == 'image_dockerfile':
                    file_info = args.dockerfile_path
                elif args.image_data_type == 'image_analysis_file':
                    file_info = args.image_analysis_file
                if file_info:
                    try:
                        attach_files.append(
                            ('files',
                             (file_info.split('/')[-1].split('.')[0], open(file_info, 'rb'),)),
                        )
                    except Exception as e:
                        logger.error(e)
            elif args.image_data_type == 'image_name':
                pass
            else:
                pass
        else:
            logger.info('在本地执行相应的分析操作')
            if args.image_data_type in ['image_file', 'image_dockerfile', 'image_analysis_file']:
                image_file = args.image_file
                image_dockerfile = args.dockerfile_path
                image_analysis_file = args.image_analysis_file
                # sca部分
                logger.info('开始在本地执行镜像SCA分析')
                for tool in ['syft', 'trivy']:
                    pass
                    detector.image_analysis(src_dir=args.source, tool=tool, analysis_type='sca',
                                            image_info=image_info,
                                            image_file=image_file, sca_result_file=None,
                                            dockerfile_path=None)
                # 可执行文件分析
                detector.image_analysis(src_dir=args.source, tool='custom', analysis_type='exec',
                                        image_info=image_info,
                                        image_file=image_file, sca_result_file=None,
                                        dockerfile_path=None)
                # 获取dockerfile文件
                detector.image_analysis(src_dir=args.source, tool='custom', analysis_type='dockerfile',
                                        image_info=image_info,
                                        image_file=image_file, sca_result_file=None,
                                        dockerfile_path=image_dockerfile)
                if 'image_vul' in args.type:
                    logger.info('开始在本地执行镜像漏洞检测部分（以sca结果进行漏洞检测）')
                    for tool in ['grype', 'trivy']:
                        detector.image_analysis(src_dir=args.source, tool=tool, analysis_type='vul_by_sbom',
                                                image_info=image_info,
                                                image_file=image_file, sca_result_file=None,
                                                dockerfile_path=None)

                zip_folder(DATA_DIR)
                target_file = DATA_DIR.rstrip('/') + '.zip'
                logger.info('将结果文件打包生成的路径为-{}'.format(target_file))
                try:
                    attach_files.append(
                        ('files', (target_file.split('/')[-1], open(target_file, 'rb'),)),
                    )
                except Exception as e:
                    logger.error(e)
            elif args.image_data_type == 'image_name':
                logger.info('本地执行以镜像名进行的镜像检测待实现')

        # 发起相应的检测请求
        logger.info('在服务端执行相应的分析操作，并执行相应的规则检测匹配')
        if attach_files:
            upload_status = detector.upload_files(attach_files)
            file_pk_list = [str(i.get('pk')) for i in upload_status.get('data', [])]
            data['attach_files'] = ','.join(file_pk_list)
        scan_status = detector.detect(data)
        print(scan_status)
    # 单独的扫描结果检测（sbom_syft/sbom_trivy/trivy_vul）
    elif args.type in ['image_scan_result_detect']:
        image_analysis_file = args.image_analysis_file
        if image_analysis_file:
            try:
                attach_files.append(
                    ('files', (image_analysis_file.split('/')[-1], open(image_analysis_file, 'rb'),)),
                )
            except Exception as e:
                logger.error(e)
        if attach_files:
            upload_status = detector.upload_files(attach_files)
            file_pk_list = [str(i.get('pk')) for i in upload_status.get('data', [])]
            data['attach_files'] = ','.join(file_pk_list)
        scan_status = detector.detect(data)
        print(scan_status)
        with open('detect_result.json', 'w') as f:
            try:
                f.write(json.dumps(scan_status))
            except Exception as e:
                logger.error(e)
    else:
        pass
if __name__ == '__main__':
    main()
