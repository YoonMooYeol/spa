import asyncio
from typing import List, Any

from langchain.tools import DuckDuckGoSearchRun
from langgraph.graph import Graph
from langgraph.prebuilt import ToolExecutor

# 각 노드가 수행할 함수 정의 (간단한 문자열 결합 예제)
async def node_a(input_msg: str) -> str:
    """첫 번째 노드: 입력 메시지에 'Hello, '를 추가"""
    return "Hello, " + input_msg

async def node_b(input_msg: str) -> str:
    """두 번째 노드: 이전 노드의 결과에 '!'를 추가"""
    return input_msg + "!"

async def run_simple_workflow(input_message: str):
    # 그래프 생성
    workflow = Graph()

    # 노드 추가
    workflow.add_node("node_a", node_a)
    workflow.add_node("node_b", node_b)

    # 엣지(edge) 추가: 노드 간의 연결 정의
    workflow.set_entry_point("node_a")
    workflow.add_edge("node_a", "node_b")

    # 그래프 컴파일
    compiled_workflow = workflow.compile()

    # 워크플로우 실행
    result = await compiled_workflow.ainvoke(input_message)
    print(f"Simple Workflow Result: {result}")

# Tool을 사용하는 경우의 예시
search_tool = DuckDuckGoSearchRun()
tool_executor = ToolExecutor(tools=[search_tool])

async def search_node(queries: List[str]) -> List[Any]:
    """검색 도구를 실행하는 노드, 오류 처리 추가"""
    results = []
    for query in queries:
        try:
            result = await asyncio.to_thread(tool_executor.invoke, {"name": search_tool.name, "args": {"query": query}})
            results.append(result)
        except Exception as e:
            print(f"Error during search for '{query}': {e}")
            results.append(f"Error: {e}")  # 오류 메시지 추가
    return results

async def run_tool_workflow(search_queries: List[str]):
    workflow_with_tool = Graph()
    workflow_with_tool.add_node("search", search_node)
    workflow_with_tool.set_entry_point("search")
    compiled_tool_workflow = workflow_with_tool.compile()
    result = await compiled_tool_workflow.ainvoke(search_queries)
    print(f"Tool Workflow Result: {result}")

# 메인 함수 (asyncio.run을 사용하여 비동기 함수 실행)
async def main():
    await run_simple_workflow("World")
    await run_tool_workflow(["What is LangGraph?", "What is DuckDuckGo?"])

if __name__ == "__main__":
    asyncio.run(main())