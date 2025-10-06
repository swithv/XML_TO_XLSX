"""
Módulo responsável pelo upload e extração de arquivos
"""
import zipfile
import tempfile
from pathlib import Path
from typing import List, Tuple
import config
from utils.logger import logger
from utils.validators import validate_file_extension

class UploadHandler:
    """Gerencia upload e extração de arquivos XML e ZIP"""
    
    def __init__(self):
        self.temp_dir = config.TEMP_DIR
        self.extracted_files = []
    
    def process_uploads(self, uploaded_files) -> Tuple[List[Tuple[str, bytes]], List[str]]:
        """
        Processa arquivos enviados pelo usuário
        
        Args:
            uploaded_files: Lista de arquivos do Streamlit uploader
            
        Returns:
            Tupla contendo (lista de (nome, conteúdo), lista de erros)
        """
        xml_files = []
        errors = []
        
        if not uploaded_files:
            return xml_files, ["Nenhum arquivo enviado"]
        
        for uploaded_file in uploaded_files:
            try:
                filename = uploaded_file.name
                file_content = uploaded_file.read()
                
                # Se for ZIP, extrai e processa XMLs internos
                if filename.lower().endswith('.zip'):
                    extracted = self._extract_zip(filename, file_content)
                    xml_files.extend(extracted)
                    logger.info(f"ZIP extraído: {filename} ({len(extracted)} XMLs)")
                
                # Se for XML, adiciona diretamente
                elif filename.lower().endswith('.xml'):
                    xml_files.append((filename, file_content))
                    logger.info(f"XML carregado: {filename}")
                
                else:
                    errors.append(f"Tipo de arquivo não suportado: {filename}")
            
            except Exception as e:
                errors.append(f"Erro ao processar {uploaded_file.name}: {str(e)}")
                logger.error(f"Erro ao processar arquivo: {e}")
        
        return xml_files, errors
    
    def _extract_zip(self, zip_name: str, zip_content: bytes) -> List[Tuple[str, bytes]]:
        """
        Extrai XMLs de um arquivo ZIP
        
        Args:
            zip_name: Nome do arquivo ZIP
            zip_content: Conteúdo binário do ZIP
            
        Returns:
            Lista de tuplas (nome_arquivo, conteúdo_xml)
        """
        xml_files = []
        
        try:
            # Cria arquivo temporário para o ZIP
            with tempfile.NamedTemporaryFile(delete=False, suffix='.zip') as tmp_zip:
                tmp_zip.write(zip_content)
                tmp_zip_path = tmp_zip.name
            
            # Extrai conteúdo
            with zipfile.ZipFile(tmp_zip_path, 'r') as zip_ref:
                for file_info in zip_ref.filelist:
                    # Ignora diretórios e arquivos ocultos
                    if file_info.is_dir() or file_info.filename.startswith('.'):
                        continue
                    
                    # Processa apenas XMLs
                    if file_info.filename.lower().endswith('.xml'):
                        xml_content = zip_ref.read(file_info.filename)
                        # Usa apenas o nome do arquivo, não o path completo
                        filename = Path(file_info.filename).name
                        xml_files.append((filename, xml_content))
            
            # Remove arquivo temporário
            Path(tmp_zip_path).unlink(missing_ok=True)
        
        except zipfile.BadZipFile:
            logger.error(f"Arquivo ZIP corrompido: {zip_name}")
        except Exception as e:
            logger.error(f"Erro ao extrair ZIP: {e}")
        
        return xml_files
    
    def cleanup(self):
        """Remove arquivos temporários"""
        try:
            for file in self.extracted_files:
                Path(file).unlink(missing_ok=True)
            self.extracted_files.clear()
        except Exception as e:
            logger.error(f"Erro ao limpar arquivos temporários: {e}")